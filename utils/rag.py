from langchain_chroma import Chroma
from models.embeddings import get_embeddings
from config.config import CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RESULTS

def get_retriever():
    """Load the pre-built ChromaDB vectorstore and return a retriever."""
    try:
        vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=get_embeddings(),
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": TOPK_K_RESULTS})
        return retriever
    except Exception as e:
        raise RuntimeError(f"Failed to load Vectorstore: {e}")
    
    
def retrieve_context(query:str) -> str:
    """Fetch relevant chunks from vectorstore and return as plain text."""
    try:
        retriever = get_retriever()
        docs = retriever.invoke(query)
        if not docs:
            return "No relevant information found in the knowledge base."
        return "\n\n".join(doc.page_content for doc in docs)
    except Exception as e:
        return f"[RAG error: {e}]"