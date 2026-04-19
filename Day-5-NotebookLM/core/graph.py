import streamlit as st
from langchain_ollama import ChatOllama

MODEL_NAME = "qwen2.5:0.5b"


def run_graph(query, selected_docs=None, web_search_enabled=False):
    """
    Simplified LangGraph replacement.
    Handles:
    - Document retrieval
    - LLM response
    """

    if "db" not in st.session_state:
        return {
            "answer": "No documents uploaded.",
            "sources": []
        }

    # Retrieve documents
    docs = st.session_state["db"].similarity_search(query, k=4)

    # Filter selected docs
    if selected_docs:
        docs = [d for d in docs if d.metadata.get("filename") in selected_docs]

    # Prepare context
    context = "\n\n".join([d.page_content for d in docs])

    # Prepare sources
    sources = []
    for d in docs:
        sources.append({
            "filename": d.metadata.get("filename", ""),
            "page_number": d.metadata.get("page_number", ""),
            "snippet": d.page_content[:200]
        })

    # LLM
    llm = ChatOllama(model=MODEL_NAME)

    response = llm.invoke(
        f"Answer ONLY from this context:\n\n{context}\n\nQuestion: {query}"
    )

    return {
        "answer": response.content,
        "sources": sources
    }


def get_graph_mermaid():
    """
    Dummy graph visualization (for UI)
    """
    return """
    graph TD
        A[User Query] --> B[Retrieve Documents]
        B --> C[Generate Answer]
        C --> D[Return Response]
    """