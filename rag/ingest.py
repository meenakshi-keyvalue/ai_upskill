# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.vectorstores import Chroma
# import os

# def ingest_contract(contract_text: str, doc_id: str):
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
#     chunks = splitter.split_text(contract_text)

#     embeddings = OpenAIEmbeddings()
#     vectordb = Chroma(persist_directory="./vectordb", embedding_function=embeddings)

#     docs = [{"page_content": chunk, "metadata": {"doc_id": doc_id}} for chunk in chunks]
#     vectordb.add_texts([d["page_content"] for d in docs], metadatas=[d["metadata"] for d in docs])
#     vectordb.persist()
#     print("✅ Vector DB created and persisted!")

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def ingest_text_into_vectordb(contract_text: str, doc_id: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(contract_text)

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory="./db", embedding_function=embeddings)

    docs = [{"page_content": chunk, "metadata": {"doc_id": doc_id}} for chunk in chunks]
    vectordb.add_texts(
        texts=[d["page_content"] for d in docs],
        metadatas=[d["metadata"] for d in docs]
    )
    vectordb.persist()
    print(f"✅ Ingested {len(chunks)} chunks for doc_id={doc_id}")

