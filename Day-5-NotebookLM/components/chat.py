import streamlit as st
from core.rag_chain import rag_query
from tavily import TavilyClient
import os
import re
from datetime import datetime


def clean_text(text):
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"http\S+", "", text)
    text = text.replace("Your browser doesn't support HTML5 audio.", "")
    return text.strip()


def save_note(answer, question):
    notes_dir = "storage/notes"
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    title = question[:50].replace(" ", "_")

    filename = f"{title}_{timestamp}.md"
    filepath = os.path.join(notes_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {question}\n\n")
        f.write(f"{timestamp}\n\n")
        f.write(answer)

    return filename


def is_relevant(question, answer):
    q_words = set(question.lower().split())
    a_words = set(answer.lower().split())

    common = q_words.intersection(a_words)

    return len(common) >= 2   # threshold


def render_chat():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # show history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # input
    if prompt := st.chat_input("Ask anything..."):

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                answer = ""
                sources = []
                use_web = False

               
                if "db" in st.session_state:

                    result = rag_query(
                        question=prompt,
                        selected_files=st.session_state.get("selected_files", [])
                    )

                    answer = result["answer"]
                    sources = result.get("sources", [])

                    if not is_relevant(prompt, answer):
                        use_web = True

                else:
                    use_web = True

               
                if use_web and st.session_state.get("web"):

                    try:
                        client = TavilyClient(api_key="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")
                        response = client.search(
                            query=prompt,
                            search_depth="advanced",
                            max_results=3
                        )

                        answer = ""

                        for r in response["results"]:
                            cleaned = clean_text(r["content"])

                            if len(cleaned) < 50:
                                continue

                            answer += f"🔗 **{r['title']}**\n{cleaned[:250]}...\n\n"

                        if answer.strip() == "":
                            answer = "❌ No useful web results found."

                    except Exception as e:
                        answer = f"❌ Web error: {str(e)}"

                
                if not answer:
                    answer = " No relevant answer found."

            # show answer
            st.markdown(answer)

            if sources and not use_web:
                with st.expander("Sources"):
                    for s in sources:
                        st.caption(f"{s['filename']} - Page {s['page_number']}")
                        st.text(s["snippet"])

            if st.button("Save as Note", key=f"save_{len(st.session_state.messages)}"):
                filename = save_note(answer, prompt)
                st.success(f"Saved: {filename}")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })