import json
from dotenv import load_dotenv

from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.chat_models import ChatOllama

# load environment variables
load_dotenv()

# initialize model
llm = ChatOllama(model="tinyllama", temperature=0)

# web search tool
search = TavilySearchResults()

@tool
def web_search(query: str) -> str:
    """Search latest information from web"""
    return str(search.invoke(query))

# summarize tool
@tool
def summarize(text: str) -> str:
    """Summarize given text"""
    prompt = f"Summarize this in short:\n{text}"
    return llm.invoke(prompt).content


# notes tool
@tool
def notes(text: str) -> str:
    """Convert text into notes format"""
    prompt = f"""
Convert into notes:

Text: {text}

Output:
Title:
Content:
"""
    return llm.invoke(prompt).content


# agent logic
def run_agent(query):
    print("\n" + "="*50)
    print("User:", query, "\n")

    query_lower = query.lower()

    # web search case
    if "news" in query_lower:
        print("Tool used: web_search")

        result = web_search.invoke({"query": query})
        print("Tool output:", result)

        print("\nTool used: summarize")

        summary = summarize.invoke({"text": result})
        print("\nFinal Answer:", summary)

    # summarize case
    elif "summarize" in query_lower:
        print("Tool used: summarize")

        result = summarize.invoke({"text": query})
        print("\nFinal Answer:", result)

    # notes case
    elif "notes" in query_lower:
        print("Tool used: notes")

        result = notes.invoke({"text": query})
        print("\nFinal Answer:", result)

    # default case
    else:
        print("Tool used: summarize")

        result = summarize.invoke({"text": query})
        print("\nFinal Answer:", result)


# test queries
if __name__ == "__main__":

    print("\nDay 4 Tool Calling Output\n")
    run_agent("What is the latest news on OpenAI?")
    run_agent("Summarize this paragraph: Artificial Intelligence is transforming industries through automation and decision making.")
    run_agent("Find the latest news on AI agents and summarize it")
    run_agent("Convert this into notes: AI improves efficiency and automates repetitive tasks.")
    run_agent("What is the difference between local models and API-based models?")