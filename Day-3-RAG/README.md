# Day 3 — RAG (Retrieval-Augmented Generation)

#🚀 What I Learned

* Converting text chunks into embeddings
* Storing embeddings in a vector database (ChromaDB)
* Understanding semantic search (meaning-based retrieval)
* Building a retriever to fetch top-k relevant chunks
* Creating a complete RAG pipeline using LLM

#🛠️ Task
Built a RAG pipeline that retrieves relevant document chunks and generates answers using a local LLM (TinyLlama via Ollama).

#🔥 Features

* Load and process PDF documents
* Generate embeddings using Ollama (nomic-embed-text)
* Store vectors in ChromaDB
* Retrieve top-k relevant chunks using semantic similarity
* Generate answers using retrieved context

#📁 Files
doc_rag.py
requirements.txt

#🎯 Key Insight
RAG is not about memorizing data — it’s about retrieving the *right context* and letting the LLM generate accurate answers from it.

