import os
import argparse
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from models.embeddings import get_embeddings
from config.config import CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def ingest_file(file_path: str) -> int:
    """Load and chunk a single PDF or TXT file. Returns chunk count."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    else:
        print(f"Skipping unsupported file: {file_path}")
        return 0

    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(docs)


def ingest(path: str):
    try:
        all_chunks = []

        # If path is a folder — process all files inside
        if os.path.isdir(path):
            files = [os.path.join(path, f) for f in os.listdir(path)]
            for file_path in files:
                print(f"Loading: {file_path}")
                chunks = ingest_file(file_path)
                all_chunks.extend(chunks)
                print(f"  → {len(chunks)} chunks")

        # If path is a single file
        elif os.path.isfile(path):
            print(f"Loading: {path}")
            chunks = ingest_file(path)
            all_chunks.extend(chunks)
            print(f"  → {len(chunks)} chunks")

        else:
            raise ValueError(f"Path not found: {path}")

        if not all_chunks:
            print("No chunks to embed. Check your files.")
            return

        print(f"\nTotal chunks to embed: {len(all_chunks)}")
        print("Embedding and saving to ChromaDB...")

        Chroma.from_documents(
            documents=all_chunks,
            embedding=get_embeddings(),
            persist_directory=CHROMA_DIR,
        )
        print(f"Done! Vectorstore saved to '{CHROMA_DIR}/'")

    except Exception as e:
        print(f"Ingestion failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="Path to a file OR a folder of files")
    args = parser.parse_args()
    ingest(args.path)