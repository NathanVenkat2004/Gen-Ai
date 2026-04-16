# Day 4 — Tool Calling Agent

## 🚀 What I Learned

- Defining tools using LangChain `@tool` decorator  
- Understanding how LLMs decide which tool to use  
- Building a manual tool-calling agent loop  
- Parsing and executing tool calls from LLM output  
- Chaining multiple tools (web search → summarize)  

---

## 🛠️ Task

Built a Tool Calling Agent that selects and executes tools like web search, summarization, and notes generation using TinyLlama (Ollama).

---

## 🔥 Features

- Web search using Tavily API  
- Summarization using local LLM (TinyLlama)  
- Notes generation from text  
- Manual agent loop for tool execution  
- Multi-step tool chaining (search + summarize)  

---

## 📁 Files

- day4_tool_calling.py  

---

## 🎯 Key Insight

Tools are simple Python functions.  
The LLM decides **which tool to call**, but the **actual execution is handled by the code**.
