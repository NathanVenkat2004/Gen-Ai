# Imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate


print("Loading document...\n")

pdf_path = "pdfs/Complaint-and-Severity-Identification-from-Online-Financial-Content.pdf"

loader = PyPDFLoader(pdf_path)
documents = loader.load()

print(f"Loaded {len(documents)} pages")


print("\nSplitting...\n")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

print(f"Total chunks: {len(chunks)}")


print("\nCreating embeddings...\n")

embedding = OllamaEmbeddings(model="nomic-embed-text")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="./chroma_db"
)

print("Vector DB created!")


retriever = vector_db.as_retriever(search_kwargs={"k": 2})


print("\nBuilding RAG...\n")

llm = ChatOllama(
    model="tinyllama",
    temperature=0,
    num_predict=50
)

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Answer using ONLY the context.

Context:
{context}

Question:
{question}

Answer:
"""
)


def generate_answer(question):
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content[:120] for doc in docs])

    final_prompt = prompt.format(context=context, question=question)

    response = llm.invoke(final_prompt)

    return docs, response.content


print("\nTesting...\n")

questions = [
    "What is complaint detection?",
    "What techniques are used in the paper?",
    "Why is complaint classification important?"
]

for q in questions:
    print("=" * 50)
    print(f"Question: {q}\n")

    docs, answer = generate_answer(q)

    print("Top Chunk:\n")
    for doc in docs:
        print(doc.page_content[:200])

    print("\nAnswer:\n")
    print(answer)
    print("\n")