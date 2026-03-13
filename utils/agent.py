from typing import Annotated, TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from models.llm import get_llm
from utils.search import web_search
from utils.rag import retrieve_context



@tool
def search_web(query:str) -> str:
    """Search the web for recent information relevant to the query."""
    return web_search(query)

@tool
def search_documents(query:str) -> str:
    """Search the knowledge base for relevant information."""
    result = retrieve_context(query)
    return result if result else "No relevant content found in the knowledge base."


TOOLS = [search_web, search_documents]

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    
    
#NODES

def call_llm(state:AgentState,llm):
    """Call the LLM with the current conversation history and return the response."""
    response = llm.invoke(state["messages"])
    return {"messages":[response]}

def call_tools(state:AgentState):
    """Node 2 — run whatever tool the LLM requested."""
    last_message = state["messages"][-1]
    tool_map = {t.name: t for t in TOOLS}
    results = []
    
    for tool_call in last_message.tool_calls:
        tool_fn = tool_map.get(tool_call["name"])
        if tool_fn:
            output = tool_fn.invoke(tool_call["args"])
        else:
            output = "Tool not found."
        results.append(ToolMessage(content=str(output), tool_call_id=tool_call["id"]))

    return {"messages": results}


def should_continue(state:AgentState):
    """Edge condition — did the LLM call a tool or is it done?"""
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END


#workflow

def build_agent():
    try:
        llm = get_llm().bind_tools(TOOLS)  # tell LLM about the tools

        # Wrap call_llm so it has access to llm
        def llm_node(state: AgentState):
            return call_llm(state, llm)

        graph = StateGraph(AgentState)

        # Add nodes
        graph.add_node("llm", llm_node)
        graph.add_node("tools", call_tools)

        # Set starting node
        graph.set_entry_point("llm")

        # Add edges
        graph.add_conditional_edges("llm", should_continue)  # llm → tools or END
        graph.add_edge("tools", "llm")  # after tools, always go back to llm

        return graph.compile()
    except Exception as e:
        raise RuntimeError(f"Failed to build agent: {e}")


AGENT = None

def get_agent():
    global AGENT
    if AGENT is None:
        AGENT = build_agent()
    return AGENT



def chat(history: List[BaseMessage], user_input: str, mode: str = "detailed") -> str:
    """
    Main function called by app.py.
    Takes chat history, new user message, and response mode.
    Returns the assistant's reply as a string.
    """
    try:
        # Mode instruction changes how the LLM responds
        if mode == "concise":
            mode_instruction = "Reply in 2-3 short sentences. Be direct and to the point."
        else:
            mode_instruction = "Provide a thorough, well-structured answer with explanations and examples where helpful."

        system = SystemMessage(content=(
            "You are a helpful AI assistant with access to two tools:\n"
            "1. search_web — use this for current/real-time information\n"
            "2. search_documents — use this when the user asks about the knowledge base\n"
            f"{mode_instruction}"
        ))

        messages = [system] + history + [HumanMessage(content=user_input)]
        result = get_agent().invoke({"messages": messages})
        return result["messages"][-1].content

    except Exception as e:
        return f"Sorry, something went wrong: {e}"