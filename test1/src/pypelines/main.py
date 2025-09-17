from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="pypelines")

    @app.get("/")
    async def root():
        return {"ok": True}

    return app


# Expose the app instance for uvicorn: pypelines.main:app
app = create_app()
