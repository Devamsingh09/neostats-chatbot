from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    """Return a free HuggingFace embedding model (runs locally, no API key needed)."""
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"})
        
        return embeddings
    
    except Exception as e:
        raise RuntimeError(f"Failed to initialize HuggingFace Embeddings: {e}")
