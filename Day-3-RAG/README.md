# Day 3 — Retrieval-Augmented Generation (RAG)

🚀 **What I Learned**

- Converting document chunks into embeddings  
- Storing embeddings in ChromaDB  
- Understanding semantic search (search by meaning, not keywords)  
- Building a retriever to fetch top-k relevant chunks  
- Creating a complete RAG pipeline using LLM  

🛠️ **Task**

Built a Retrieval-Augmented Generation (RAG) pipeline that retrieves relevant document chunks and generates answers using TinyLlama (via Ollama).

🔥 **Features**

- Process PDF documents into chunks  
- Generate embeddings using nomic-embed-text  
- Store vectors in ChromaDB  
- Retrieve top-k relevant chunks using semantic similarity  
- Generate answers using retrieved context + LLM  

📁 **Files**

- doc_rag.py  
- requirements.txt  

🎯 **Key Insight**

RAG is not about memorizing data — metadata and embeddings help retrieve the most relevant context, and the LLM uses that to generate accurate answers.
