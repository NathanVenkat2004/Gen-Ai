import streamlit as st
from components.sidebar import render_sidebar
from components.chat import render_chat
from components.notes import render_notes
from core.graph import get_graph_mermaid
st.set_page_config(
    page_title="NotebookLM",
    page_icon="📓",
    layout="wide"
)
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "selected_files" not in st.session_state:
    st.session_state["selected_files"] = []

if "web" not in st.session_state:
    st.session_state["web"] = False
st.title("📓 NotebookLM")
st.caption("Upload PDFs → Ask questions → Get grounded answers")
render_sidebar()
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📝 Notes", "⚙️ Workflow"])
with tab1:
    render_chat()

with tab2:
    render_notes()

with tab3:
    st.header("Workflow")

    try:
        graph = get_graph_mermaid()
        st.code(graph, language="mermaid")
    except:
        st.info("Simple workflow visualization enabled")