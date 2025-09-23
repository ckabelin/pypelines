import os
import pytest

from pypelines import ai


@pytest.mark.skipif(not getattr(ai, "LANGCHAIN_AVAILABLE", False), reason="langchain/chroma not installed")
def test_chroma_add_and_search(tmp_path):
    persist = tmp_path / "chroma_store"
    db = ai.ChromaVectorDB(persist_directory=str(persist), collection_name="testcol")
    texts = ["This is a test document about Python.", "Another doc about FastAPI and uvicorn."]
    metas = [{"title": "python"}, {"title": "fastapi"}]
    db.add_documents(texts, metas)
    results = db.similarity_search("FastAPI server")
    assert len(results) > 0


@pytest.mark.skipif(not getattr(ai, "LANGCHAIN_AVAILABLE", False), reason="langchain/chroma not installed")
def test_export_import(tmp_path):
    persist = tmp_path / "chroma_store2"
    db = ai.ChromaVectorDB(persist_directory=str(persist), collection_name="testcol2")
    texts = ["Alpha Beta Gamma", "Delta Epsilon Zeta"]
    db.add_documents(texts)
    export_path = tmp_path / "export.json"
    db.export(str(export_path))
    assert export_path.exists()

    # import into new store
    db2 = ai.ChromaVectorDB(persist_directory=str(tmp_path / "chroma_store3"), collection_name="testcol3")
    db2.import_from(str(export_path))
    res = db2.similarity_search("Alpha")
    assert len(res) > 0
