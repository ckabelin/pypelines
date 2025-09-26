from fastapi import FastAPI, UploadFile, File, HTTPException
from pypelines.ai import ChromaVectorDB, OllamaWrapper
from typing import List
import os


PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_store")
DB = None
LLM = None


def create_app() -> FastAPI:
    app = FastAPI(title="pypelines")

    @app.on_event("startup")
    async def startup_event():
        global DB, LLM
        try:
            DB = ChromaVectorDB(persist_directory=PERSIST_DIR)
        except Exception:
            DB = None
        try:
            LLM = OllamaWrapper()
        except Exception:
            LLM = None

    @app.get("/")
    async def root():
        return {"ok": True}

    @app.post("/vector/add")
    async def add_documents(texts: List[str]):
        if DB is None:
            raise HTTPException(status_code=500, detail="Vector DB not available")
        DB.add_documents(texts)
        return {"added": len(texts)}

    @app.post("/vector/import")
    async def import_vector(file: UploadFile = File(...)):
        if DB is None:
            raise HTTPException(status_code=500, detail="Vector DB not available")
        contents = await file.read()
        path = f"/tmp/{file.filename}"
        with open(path, "wb") as f:
            f.write(contents)
        DB.import_from(path)
        os.remove(path)
        return {"imported": True}

    @app.get("/vector/export")
    async def export_vector():
        if DB is None:
            raise HTTPException(status_code=500, detail="Vector DB not available")
        path = "/tmp/pypelines_vectors.json"
        DB.export(path)
        return {"exported_path": path}

    @app.post("/vector/clear")
    async def clear_vector():
        # remove persisted directory
        if DB is None:
            raise HTTPException(status_code=500, detail="Vector DB not available")
        if DB.persist_directory and os.path.exists(DB.persist_directory):
            import shutil

            shutil.rmtree(DB.persist_directory)
            DB._init_store()
        return {"cleared": True}

    @app.post("/chat")
    async def chat(query: str):
        if LLM is None:
            raise HTTPException(status_code=500, detail="LLM not available")
        context = DB.similarity_search(query) if DB is not None else []
        context_text = "\n\n".join([d.page_content for d in context])
        prompt = f"Use the following context to answer the question:\n{context_text}\n\nUser: {query}\nAssistant:" if context_text else f"User: {query}\nAssistant:"
        resp = LLM.complete(prompt)
        return {"answer": resp}

    return app



# Expose the app instance for uvicorn: pypelines.main:app
app = create_app()
