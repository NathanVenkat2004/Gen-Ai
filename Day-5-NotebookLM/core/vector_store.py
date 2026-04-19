from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings

CHROMA_DIR = "storage/chroma_db"


def get_embeddings():
    return FakeEmbeddings(size=384)


def create_vector_db(chunks):
    db = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=CHROMA_DIR
    )
    return db