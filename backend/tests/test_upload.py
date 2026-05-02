import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app

@pytest.mark.asyncio
async def test_upload_too_many_files():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        files = [("files", ("test.pdf", b"dummy", "application/pdf")) for _ in range(6)]
        response = await ac.post("/api/v1/analyze", files=files)
        assert response.status_code == 400
        assert "Maximum 5 files allowed" in response.json()["detail"]

@pytest.mark.asyncio
async def test_upload_wrong_type():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        files = [("files", ("test.txt", b"dummy", "text/plain"))]
        response = await ac.post("/api/v1/analyze", files=files)
        assert response.status_code == 400
        assert "File type .txt not allowed" in response.json()["detail"]

# Need to mock celery delay for successful upload
# But we can test it handles correct type basically
