from langgraph.graph import StateGraph
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from typing import TypedDict

class RAGState(TypedDict):
    question: str
    context: str
    answer: str
    docs: str


retriever = Chroma(persist_directory="./db", embedding_function=OpenAIEmbeddings()).as_retriever()

qa_prompt = PromptTemplate.from_template("""
Answer the question based only on the context provided.

Context:
{context}

Question:
{question}
""")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# LangGraph nodes
def retrieve_docs(state):
    # docs = retriever.get_relevant_documents(state["question"])
    # return {"docs": docs, "question": state["question"]}
    docs = retriever.get_relevant_documents(state["question"])
    print(f"🔍 Retrieved {len(docs)} docs for query: {state['question']}")
    for i, d in enumerate(docs):
        print(f"Doc {i+1}: {d.page_content}...")  # Preview first 100 chars
    return {"docs": docs, "question": state["question"]}

def generate_answer(state):
    if "docs" not in state or not state["docs"]:
        return {"answer": "❌ No documents found to generate answer."}
    context = "\n\n".join([doc.page_content for doc in state["docs"]])
    result = llm.invoke(qa_prompt.format(context=context, question=state["question"]))
    return {"answer": result.content}

# Define LangGraph
def get_query_graph():
    graph = StateGraph(RAGState)
    graph.add_node("retrieve", retrieve_docs)
    graph.add_node("generate", generate_answer)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.set_finish_point("generate")

    return graph.compile()
