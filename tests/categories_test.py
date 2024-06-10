import pytest

@pytest.mark.asyncio
async def test_get_404(client, test_db):
    async for client_instance in client:
        response = await client_instance.get("/categories/1")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_create(client, test_db):
    async for client_instance in client:
        valid_data = {"name": "New Category"}
        response_create_valid = await client_instance.post("/categories", json=valid_data)
        assert response_create_valid.status_code == 201

        response_get = await client_instance.get("/categories/1")
        assert response_get.status_code == 200

        # response_create = await client_instance.post("/categories", json={})
        # assert response_create.status_code == 401

# @pytest.mark.asyncio
# async def test_get_by_id(client, test_db):
#     async for client_instance in client:
#         response = await client_instance.get("/categories/20000")
#         assert response.status_code == 200

# @pytest.mark.asyncio
# async def test_get_all(client, test_db):
#     async for client_instance in client:
#         response = await client_instance.get("/categories")
#         assert response.status_code == 200

# @pytest.mark.asyncio
# async def test_patch(client, test_db):
#     async for client_instance in client:
#         response = await client_instance.patch("/categories/1")
#         assert response.status_code == 200
