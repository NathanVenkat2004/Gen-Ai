
SYSTEM_PROMPT = """Answer shortly using the document.
If not found, say 'Not found'."""



QA_PROMPT_TEMPLATE = """
Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}

Answer:
"""

SUMMARY_PROMPT = """
Convert the following answer into a short note.

- Keep important points
- Use bullet format
- Keep it under 150 words

Answer:
{response}

Note:
"""


WEB_SEARCH_PROMPT = """
Use both document context and web results to answer.

Document Context:
{context}

Web Results:
{web_results}

Question:
{question}

Answer:
"""