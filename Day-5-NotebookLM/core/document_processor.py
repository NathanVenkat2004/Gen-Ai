from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Simple constants (remove config dependency)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()


def chunk_documents(pages, filename):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(pages)

    upload_date = datetime.now().isoformat()

    for chunk in chunks:
        chunk.metadata["filename"] = filename
        chunk.metadata["upload_date"] = upload_date
        chunk.metadata["page_number"] = chunk.metadata.get("page", 0) + 1

    return chunks


def process_pdf(file_path, filename):
    pages = load_pdf(file_path)
    return chunk_documents(pages, filename)


# 🔥 IMPORTANT (for your sidebar compatibility)
def load_and_split(file_path):
    filename = file_path.split("\\")[-1]
    return process_pdf(file_path, filename)