import streamlit as st
import os
from core.document_processor import load_pdf, chunk_documents
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

UPLOADS_DIR = "storage/uploads"


def render_sidebar():

    st.sidebar.header("Documents")

    uploaded_files = st.sidebar.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    selected_files = []

    if uploaded_files and "db" not in st.session_state:

        all_chunks = []

        with st.spinner("Processing PDFs..."):

            for file in uploaded_files:
                file_path = os.path.join(UPLOADS_DIR, file.name)

                with open(file_path, "wb") as f:
                    f.write(file.read())

                pages = load_pdf(file_path)
                chunks = chunk_documents(pages, file.name)

                all_chunks.extend(chunks[:5])  # 🔥 limit for speed

            embeddings = OllamaEmbeddings(model="nomic-embed-text")

            db = Chroma.from_documents(
                documents=all_chunks,
                embedding=embeddings,
                persist_directory="storage/chroma_db"
            )

            st.session_state["db"] = db

        st.success("Documents processed!")

    if uploaded_files:
        st.sidebar.subheader("Select Files")

        for file in uploaded_files:
            if st.sidebar.checkbox(file.name, value=True):
                selected_files.append(file.name)

    st.session_state["selected_files"] = selected_files

    # 🌐 Web toggle
    web = st.sidebar.checkbox("Enable Web Search")
    st.session_state["web"] = web

    # 🧹 Clear chat
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

