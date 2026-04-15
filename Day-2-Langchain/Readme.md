# 📄 Day 2 — LangChain Document Processing

## 🚀 What I Learned
- Loading PDFs using LangChain
- Splitting documents into chunks
- Understanding how chunk_size and overlap works
- Attaching metadata to each chunk
- Filtering chunks using metadata

## 🛠️ Task
Built a document processing pipeline using PyPDFLoader and RecursiveCharacterTextSplitter.

## 🔥 Features
- Load multiple PDF files
- Split text into chunks (chunk_size=1000, overlap=200)
- Attach metadata (filename, page number, upload date, source type)
- Filter chunks based on metadata

## 📁 Files
- Document_loader.ipynb
- pdfs/

## 🎯 Key Insight
Chunks are not just text — metadata helps in filtering and is the base for Retrieval-Augmented Generation (RAG)
