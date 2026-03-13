# 🤖 NeoStats AI Chatbot

An intelligent conversational AI assistant built for NeoStats, powered by **Groq LLM**, **LangGraph**, **RAG**, and **Live Web Search** — deployed on Streamlit Cloud.

---

## 🔗 Links

| | |
|---|---|
| 🚀 **Live App** | https://neostats01.streamlit.app/ |
| 💻 **GitHub** | https://github.com/Devamsingh09/neostats-chatbot |

---

## 📌 Use Case

Enterprise teams waste hours searching through documents and the web to find answers. This chatbot solves that by combining:
- A **pre-loaded knowledge base** from NeoStats research documents
- **Real-time web search** for current information
- **Conversation memory** to maintain context across turns
- **Two response modes** — Concise or Detailed — based on user preference

---

## ✨ Features

### 1. 📄 RAG (Retrieval-Augmented Generation)
- NeoStats research PDFs are **pre-embedded** into ChromaDB using `ingest.py`
- Uses **HuggingFace `all-MiniLM-L6-v2`** embeddings (free, runs locally)
- LangGraph agent calls the RAG tool automatically when questions relate to documents
- Retrieves top-4 most relevant chunks per query

### 2. 🌐 Live Web Search
- Powered by **Tavily Search API**
- Agent decides when to search the web vs answer from knowledge base
- Returns top-3 clean text results to the LLM

### 3. ⚡ Response Modes
- **Concise** — Short, 2-3 sentence sharp replies
- **Detailed** — Full, structured, in-depth answers
- Toggle in the Streamlit sidebar

### 4. 🧠 Conversation Memory
- Full chat history passed to the agent on every turn
- Bot remembers what was said earlier in the conversation

---

## 🏗️ Project Structure

```
neostats_chatbot/
│
├── config/
│   └── config.py           ← All API keys and settings
│
├── models/
│   ├── llm.py              ← Groq LLM (llama-3.3-70b-versatile)
│   └── embeddings.py       ← HuggingFace embedding model
│
├── utils/
│   ├── agent.py            ← LangGraph agent (orchestrates everything)
│   ├── rag.py              ← ChromaDB retriever
│   └── search.py           ← Tavily web search
│
├── docs/                   ← Put your PDFs here
├── chroma_db/              ← Auto-created after running ingest.py
│
├── app.py                  ← Streamlit UI
├── ingest.py               ← One-time document embedding script
├── requirements.txt
└── .env                    ← Your API keys (never commit this)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Devamsingh09/neostats-chatbot.git
cd neostats-chatbot
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

Get your free API keys:
- **Groq** → https://console.groq.com
- **Tavily** → https://tavily.com

### 5. Add your documents
Place your PDF or TXT files inside the `docs/` folder.

### 6. Embed documents (one-time)
```bash
# Embed all files in the docs/ folder
python ingest.py --path docs

# Or embed a single file
python ingest.py --path docs/your_file.pdf
```

This creates the `chroma_db/` folder with your vectorstore.

### 7. Run the app
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 🧠 How It Works

```
User asks a question
        ↓
  LangGraph Agent
        ↓
  Does it need a tool?
    ↙           ↘
  YES            NO
   ↓              ↓
Which tool?    Answer directly
  ↙    ↘
RAG   Web Search
  ↓    ↓
LLM reads result
        ↓
  Returns answer
  (Concise / Detailed)
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Groq** (`llama-3.3-70b-versatile`) | LLM inference |
| **LangChain** | LLM framework & tool wiring |
| **LangGraph** | Agent orchestration (stateful graph) |
| **ChromaDB** | Vector database for RAG |
| **HuggingFace** (`all-MiniLM-L6-v2`) | Free local embeddings |
| **Tavily** | Web search API |
| **Streamlit** | UI framework |
| **python-dotenv** | Environment variable management |

---

## 🚀 Deployment

The app is deployed on **Streamlit Cloud**.

To deploy your own instance:
1. Push your code (including `chroma_db/`) to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your GitHub repo
4. Set `app.py` as the main file
5. Add secrets in **Advanced Settings**:
   ```
   GROQ_API_KEY = "your_key"
   TAVILY_API_KEY = "your_key"
   ```
6. Click Deploy

---

## 📁 Key Files Explained

| File | What it does |
|---|---|
| `config/config.py` | Central config — all keys and settings in one place |
| `models/llm.py` | Creates and returns the Groq LLM instance |
| `models/embeddings.py` | Loads the HuggingFace embedding model |
| `utils/rag.py` | Loads ChromaDB and retrieves relevant chunks |
| `utils/search.py` | Runs Tavily web search and returns plain text |
| `utils/agent.py` | LangGraph agent — wires LLM + tools + memory |
| `ingest.py` | One-time script to embed docs into ChromaDB |
| `app.py` | Streamlit UI — chat interface + response mode toggle |

---

## ⚠️ Important Notes

- **Never commit your `.env` file** — it contains your API keys
- **`chroma_db/`** should be committed if deploying to Streamlit Cloud (no persistent storage)
- Run `ingest.py` again if you add new documents to `docs/`
- The `BertModel LOAD REPORT` warning during ingestion is harmless — ignore it

---

## 👤 Author

**Devam Singh**
Built for NeoStats AI Engineer Case Study — 2026
