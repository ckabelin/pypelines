from __future__ import annotations

import json
import os
from typing import List, Optional, Dict

try:
    from langchain.schema import Document
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.llms import Ollama
    LANGCHAIN_AVAILABLE = True
except Exception:
    LANGCHAIN_AVAILABLE = False


class ChromaVectorDB:
    """Chroma-backed vector store using LangChain wrappers.

    Features:
    - document chunking with metadata
    - add_documents(texts, metadatas)
    - similarity_search(query, k)
    - export/import (JSON) for portability
    - in-process persistence via Chroma client (persist_directory optional)
    """

    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", persist_directory: Optional[str] = None, collection_name: str = "pypelines"):
        if not LANGCHAIN_AVAILABLE:
            raise RuntimeError("Required langchain/chromadb packages not installed; install the 'ai' extra.")
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self._init_store()

    def _init_store(self):
        # create or load chroma vectorstore
        if self.persist_directory:
            self.store = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings, collection_name=self.collection_name)
        else:
            self.store = Chroma(embedding_function=self.embeddings, collection_name=self.collection_name)

    def add_documents(self, texts: List[str], metadatas: Optional[List[Dict]] = None) -> None:
        if metadatas is None:
            metadatas = [{} for _ in texts]
        docs = []
        for text, meta in zip(texts, metadatas):
            # chunk the document
            pieces = self.text_splitter.split_text(text)
            for i, p in enumerate(pieces):
                m = dict(meta)
                m.update({"chunk_index": i})
                docs.append(Document(page_content=p, metadata=m))
        # LangChain Chroma accepts plain texts + metadatas when using its convenience method
        texts = [d.page_content for d in docs]
        metas = [d.metadata for d in docs]
        self.store.add_texts(texts=texts, metadatas=metas)
        if self.persist_directory:
            self.store.persist()

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        hits = self.store.similarity_search(query, k=k)
        return hits

    def export(self, path: str) -> None:
        # export collection documents and metadatas to JSON
        docs = self.store._collection.get(include=['metadatas','documents'])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(docs, f, ensure_ascii=False, indent=2)

    def import_from(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        documents = data.get("documents", [])
        metadatas = data.get("metadatas", [])
        # add texts back
        self.store.add_texts(texts=documents, metadatas=metadatas)
        if self.persist_directory:
            self.store.persist()


class OllamaWrapper:
    def __init__(self, model: str = "llama2", server_url: Optional[str] = None):
        if not LANGCHAIN_AVAILABLE:
            raise RuntimeError("LangChain or Ollama client not available; install the 'ai' extra.")
        self.model = model
        self.client = Ollama(model=model, base_url=server_url) if server_url else Ollama(model=model)

    def complete(self, prompt: str, max_tokens: int = 512) -> str:
        resp = self.client(prompt, max_tokens=max_tokens)
        return resp.get("text") if isinstance(resp, dict) else str(resp)


__all__ = ["ChromaVectorDB", "OllamaWrapper"]
