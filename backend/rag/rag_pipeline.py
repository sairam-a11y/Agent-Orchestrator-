"""
RAG Pipeline
------------
Document Loader · Embeddings · Vector Store · Retriever
"""

# ── embeddings.py ─────────────────────────────────────────────────────────────
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
load_dotenv()

CHROMA_DIR = "./chroma_db"

def get_vectorstore() -> Chroma:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )
    return Chroma(
        collection_name="platform_knowledge",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


# ── retriever.py ──────────────────────────────────────────────────────────────
from langchain_core.documents import Document
from typing import List


class RAGRetriever:
    def __init__(self):
        self.vectorstore = get_vectorstore()
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 4, "fetch_k": 12},
        )

    async def retrieve(self, query: str) -> str:
        try:
            docs: List[Document] = self.retriever.get_relevant_documents(query)
            if not docs:
                return "No relevant context found."
            return "\n\n---\n\n".join(
                f"[{d.metadata.get('source', 'unknown')}]\n{d.page_content}"
                for d in docs
            )
        except Exception:
            return ""


# ── document_loader.py ────────────────────────────────────────────────────────
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid


class DocumentLoader:
    def __init__(self):
        self.vectorstore = get_vectorstore()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=150
        )

    async def ingest(self, content: str, source: str = "user") -> str:
        doc_id = str(uuid.uuid4())
        chunks = self.splitter.split_text(content)
        documents = [
            Document(
                page_content=chunk,
                metadata={"source": source, "doc_id": doc_id},
            )
            for chunk in chunks
        ]
        self.vectorstore.add_documents(documents)
        self.vectorstore.persist()
        return doc_id

    async def ingest_file(self, filepath: str) -> str:
        with open(filepath, "r") as f:
            content = f.read()
        return await self.ingest(content, source=filepath)
