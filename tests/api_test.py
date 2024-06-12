import pytest
import httpx



@pytest.mark.asyncio
async def test_create(client: httpx.AsyncClient, superuser):
    create_data = {"name": "New Category 1"}
    response_create = await client.post(
        "/categories", json=create_data, headers=superuser)
    assert response_create.status_code == 200
        


# @pytest.mark.asyncio
# async def test_get_one(client, category_id):
#     async for client_instance, headers in client:
#         response_get = await client_instance.get(
#             f"/categories/{category_id}", headers=headers)
#         assert response_get.status_code == 200
#         assert response_get.json()["name"] == "New Category"

# @pytest.mark.asyncio
# async def test_get_all_objects(client):
#     async for client_instance, headers in client:
#         response_get_all = await client_instance.get(
#             "/categories", headers=headers)
#         assert response_get_all.status_code == 200
#         assert len(response_get_all.json()) == 1

# @pytest.mark.asyncio
# async def test_update(client, category_id):
#     async for client_instance, headers in client:
#         new_data = {"name": "Updated Category"}
#         response_patch = await client_instance.patch(
#             f"/categories/{category_id}", json=new_data, headers=headers)
#         assert response_patch.status_code == 200
#         assert response_patch.json()["name"] == "Updated Category"

# @pytest.mark.asyncio
# async def test_delete(client):
#     async for client_instance, headers in client:
#         categories = await client_instance.get("/categories", headers=headers)
#         assert categories != []

#         category_id = categories[0]["id"]
#         response_get = await client_instance.get(
#             f"/categories/{category_id}", headers=headers)
#         assert response_get.status_code == 200

#         response_delete = await client_instance.delete(
#             f"/categories/{category_id}", headers=headers)
#         assert response_delete.status_code == 200

# @pytest.mark.asyncio
# async def test_get_deleted(client):
#     category_id = 3
#     async for client_instance, headers in client:
#         response_get_deleted = await client_instance.get(
#             f"/categories/{category_id}", headers=headers)
#         assert response_get_deleted.status_code == 404  

