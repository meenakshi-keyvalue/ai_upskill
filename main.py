from fastapi import FastAPI, UploadFile, File
from extractors.text_extractor import extract_text_from_pdf_bytes
from llm.openai_extractor import extract_contract_details
from rag.ingest import ingest_text_into_vectordb
from rag.query_graph import get_query_graph
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Serve index.html at root
@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

# Optional: Serve static files (if you have CSS, JS separately later)
app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.post("/extract-contract-info")
# async def extract_contract_info(file: UploadFile = File(...)):
#     file_bytes = await file.read()
#     extracted_text = extract_text_from_pdf_bytes(file_bytes)
#     result = extract_contract_details(extracted_text)
#     return result

@app.post("/extract-contract-info")
async def extract_contract_info(file: UploadFile = File(...)):
    file_bytes = await file.read()
    extracted_text = extract_text_from_pdf_bytes(file_bytes)
    result = extract_contract_details(extracted_text)

    # Optional: use filename (without extension) as doc_id
    doc_id = file.filename.rsplit(".", 1)[0]
    ingest_text_into_vectordb(extracted_text, doc_id)

    return result


graph = get_query_graph()

class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    result = graph.invoke({"question": request.question})
    return {"answer": result["answer"]}