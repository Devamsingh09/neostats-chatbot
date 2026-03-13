import os
from dotenv import load_dotenv
load_dotenv()  


#API_KEYS
GROQ_API_KEY = os.getenv("GROQ_API_KEY","")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY","")

#GROQ Model
GROQ_MODEL  = "llama-3.3-70b-versatile" # "llama-3.3-8b-instruct" or "gemini-1.5-pro" or "gemini-2.0-pro" or "gemini-2.5-pro"
TEMPERATURE = 0.3


#RAG SETTINGS
CHROMA_DIR = "chroma_db"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K_RESULTS = 4

