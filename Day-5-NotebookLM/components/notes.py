import os
import streamlit as st

NOTES_DIR = "storage/notes"


def load_notes():
    notes = []

    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
        return notes

    for filename in sorted(os.listdir(NOTES_DIR), reverse=True):

        if filename.endswith(".md"):

            filepath = os.path.join(NOTES_DIR, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.strip().split("\n")

            title = lines[0].replace("#", "").strip() if lines else filename
            date = lines[1] if len(lines) > 1 else ""

            notes.append({
                "filename": filename,
                "title": title,
                "date": date,
                "content": content
            })

    return notes


def combine_notes(notes):
    return "\n\n---\n\n".join([n["content"] for n in notes])


def render_notes():

    st.header("📒 Notes")

    notes = load_notes()

    if not notes:
        st.info("No notes saved yet")
        return

    combined = combine_notes(notes)

    st.download_button(
        "⬇ Download All Notes",
        combined,
        file_name="notes.md"
    )

    st.divider()

    for note in notes:

        with st.expander(f"📌 {note['title']}"):

            st.caption(note["date"])

            st.markdown(note["content"])

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    "Download",
                    note["content"],
                    file_name=note["filename"]
                )

            with col2:
                if st.button("Delete", key=note["filename"]):
                    os.remove(os.path.join(NOTES_DIR, note["filename"]))
                    st.success("Deleted")
                    st.rerun()