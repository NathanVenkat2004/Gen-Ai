import streamlit as st


def format_sources(docs):
    sources = []
    seen = set()

    for d in docs:
        filename = d.metadata.get("filename", "Unknown")
        page = d.metadata.get("page_number", "?")

        key = f"{filename}-{page}"
        if key not in seen:
            seen.add(key)

            sources.append({
                "filename": filename,
                "page_number": page,
                "snippet": d.page_content[:120] + "..."
            })

    return sources


def is_relevant(question, text):
    q_words = set(question.lower().split())
    t_words = set(text.lower().split())

    common = q_words.intersection(t_words)

    return len(common) >= 1   # relaxed


def rag_query(question, selected_files=None):

    if "db" not in st.session_state:
        return {
            "answer": "",
            "sources": []
        }

    docs = st.session_state["db"].similarity_search(question, k=3)

    if selected_files:
        docs = [d for d in docs if d.metadata.get("filename") in selected_files]

    if not docs:
        return {
            "answer": "",
            "sources": []
        }

    best_doc = None

    for d in docs:
        if is_relevant(question, d.page_content):
            best_doc = d
            break

    if not best_doc:
        return {
            "answer": "",
            "sources": []
        }

    q = question.lower()
    text = best_doc.page_content

    if "how many pages" in q:
        answer = "📄 This document contains multiple pages. Exact page count cannot be determined from the retrieved content."

    elif "who is" in q:
        # avoid wrong PDF answers for person queries
        return {
            "answer": "",
            "sources": []
        }

    else:
        answer = text[:400]

    sources = format_sources([best_doc])

    return {
        "answer": answer,
        "sources": sources
    }