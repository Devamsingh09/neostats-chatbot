import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from utils.agent import chat

#page config
st.set_page_config(
    page_title="NeoStats AI Assistant",
    page_icon="🤖",
    layout="wide"
)

#Header
st.title("🤖 NeoStats AI Assistant")
st.caption("Powered by Groq · LangGraph · RAG · Web Search")

#Sidebar
with st.sidebar:
    st.divider()

    # Response mode
    st.subheader("💬 Response Mode")
    mode = st.radio(
        "Choose how the bot replies:",
        options=["detailed", "concise"],
        format_func=lambda x: "📄 Detailed — In-depth answer" if x == "detailed" else "⚡ Concise — Short & sharp",
        index=0
    )

    st.divider()
    st.info(
        "📂 **Knowledge Base:** Pre-loaded with NeoStats research documents.\n\n"
        "🌐 **Web Search:** Automatically used for real-time information.\n\n"
        "🧠 **Memory:** Conversation context is preserved."
    )
    st.divider()

    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
# ── Chat history init ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
# ── Render existing messages ──────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Ask me anything..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build LangChain message history for context
    lc_history = []
    for m in st.session_state.messages[:-1]:
        if m["role"] == "user":
            lc_history.append(HumanMessage(content=m["content"]))
        else:
            lc_history.append(AIMessage(content=m["content"]))

    # Get and show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = chat(lc_history, user_input, mode=mode)
        st.markdown(reply)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
