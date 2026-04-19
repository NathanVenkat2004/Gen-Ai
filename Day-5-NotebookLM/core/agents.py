import os
from datetime import datetime
from langchain_ollama import ChatOllama
import streamlit as st

# MODEL
MODEL_NAME = "qwen2.5:0.5b"



def document_search(query: str):
    if "db" not in st.session_state:
        return "No documents uploaded."

    docs = st.session_state["db"].similarity_search(query, k=4)

    selected = st.session_state.get("selected_files", [])
    if selected:
        docs = [d for d in docs if d.metadata.get("filename") in selected]

    context = "\n\n".join([d.page_content for d in docs])

    llm = ChatOllama(model=MODEL_NAME)

    response = llm.invoke(
        f"Answer ONLY from this context:\n\n{context}\n\nQuestion: {query}"
    )

    return response.content


def web_search(query: str):
    return f"(Web search disabled in this version)\nQuery: {query}"



def save_note(content: str):
    if not os.path.exists("storage/notes"):
        os.makedirs("storage/notes")

    filename = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join("storage/notes", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Note\n\n{content}")

    return f"Saved as {filename}"



def run_agent(query: str, web_enabled=False):
    """
    Simple decision logic instead of full ReAct agent
    """

    if web_enabled:
        return web_search(query)

    return document_search(query)