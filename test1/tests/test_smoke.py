import pytest

from pypelines import main


@pytest.mark.asyncio
async def test_root_returns_ok():
    # use FastAPI's TestClient via httpx AsyncClient
    from httpx import AsyncClient

    async with AsyncClient(app=main.app, base_url="http://test") as client:
        r = await client.get("/")
        assert r.status_code == 200
        assert r.json() == {"ok": True}
