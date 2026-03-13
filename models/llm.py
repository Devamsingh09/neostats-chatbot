from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY, GROQ_MODEL, TEMPERATURE


def get_llm():
    """Return a Groq LLM instance."""
    try:
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=TEMPERATURE,
        )
        return llm
    except Exception as e:
        raise RuntimeError(f"Failed to initialise Groq LLM: {e}")