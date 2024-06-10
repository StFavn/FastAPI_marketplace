import pytest

@pytest.mark.asyncio
async def test_get_404(client, test_db):
    async for client_instance in client:
        response = await client_instance.get("/categories/1")
        assert response.status_code == 404

