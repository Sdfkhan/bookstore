import pytest
import httpx

from main import app


@pytest.fixture(scope="module")
def app_client():
    yield app


@pytest.mark.asyncio
async def test_user_flow(app_client):
    async with httpx.AsyncClient(app=app_client, base_url="http://testserver") as client:
        # Testing signup
        response = await client.post("/signup", json={
            "name": "Sdfkhn",
            "email": "test@example.com",
            "password": "password",
        })
        assert response.status_code == 200

        # Testing login
        response = await client.post("/login", json={
            "email": "test@example.com",
            "password": "password"
        })
        token = response.json().get('access_token')
        assert token is not None

        headers = {"Authorization": f"Bearer {token}"}

        # Testing book creation
        response = await client.post("/books/", json={
            "name": "Example Book",
            "author": "Jane Doe",
            "published_year": 2023,
            "summary": "Example summary"
        }, headers=headers)
        assert response.status_code == 200

        # Testing book retrieval
        response = await client.get("/books/", headers=headers)
        assert response.status_code == 200

        # Testing book deletion
        book_id = response.json()[0]['id']  # Assuming the first book is the one we want to delete
        response = await client.delete(f"/books/{book_id}", headers=headers)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_error_handling(app_client):
    async with httpx.AsyncClient(app=app_client, base_url="http://testserver") as client:
        # Testing non-existent book
        response = await client.get("/books/invalid-id")
        assert response.status_code == 404

        # Updating non-existent book
        response = await client.put("/books/invalid-id", json={"name": "Invalid Update"})
        assert response.status_code == 404

        # Deleting book which doesn't exist
        response = await client.delete("/books/55585")  # This id doesn't exist
        assert response.status_code == 404
