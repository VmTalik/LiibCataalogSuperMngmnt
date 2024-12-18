from httpx import AsyncClient
from .messages import (
    FAILED_CREATE_AUTHOR,
    FAILED_GET_AUTHOR,
    FAILED_GET_AUTHORS,
    FAILED_UPDATE_AUTHOR,
    FAILED_DELETE_AUTHOR,
    FAILED_NUMBER_OF_AUTHORS
)


async def test_create_get_authors(ac: AsyncClient):
    number_of_authors = 15
    for i in range(number_of_authors):
        author_data = {
            "name": f"Иван_{i}",
            "surname": "Иванов",
            "date_birth": "2024-12-18",
        }
        response = await ac.post("/authors/", json=author_data)
        assert response.status_code == 201, FAILED_CREATE_AUTHOR
    response = await ac.get("/authors/?offset=0&limit=10")
    assert response.status_code == 200, FAILED_GET_AUTHORS + "offset=0&limit=10"
    assert len(response.json()) == 10, FAILED_NUMBER_OF_AUTHORS + "10"
    response = await ac.get("/authors/?offset=0&limit=20")
    assert response.status_code == 200, FAILED_GET_AUTHORS + "offset=0&limit=20"
    assert len(response.json()) == number_of_authors, f"{FAILED_NUMBER_OF_AUTHORS} {number_of_authors}"
    response = await ac.get("/authors/?offset=1&limit=15")
    assert response.status_code == 200, FAILED_GET_AUTHORS + "offset=1&limit=15"
    assert len(response.json()) == number_of_authors - 1, f"{FAILED_NUMBER_OF_AUTHORS} {number_of_authors - 1}"


async def test_create_get_author_by_id(ac: AsyncClient, author_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    response = await ac.get(f"/authors/{author_id}")
    assert response.status_code == 200, FAILED_GET_AUTHOR
    author_payload["id"] = response.json()["id"]
    author_payload["books"] = []
    assert author_payload == response.json()


async def test_create_update_author(ac: AsyncClient, author_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    author_update_data = {
        "name": f"Иван_0",
        "surname": "Иванов_0",
        "date_birth": "1724-12-18",
    }
    response = await ac.put(f"/authors/{author_id}", json=author_update_data)
    assert response.status_code == 200, FAILED_UPDATE_AUTHOR
    author_update_data["id"] = author_id
    assert response.json() == author_update_data


async def test_create_delete_author(ac: AsyncClient, author_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    response = await ac.delete(f"/authors/{author_id}")
    assert response.status_code == 204, FAILED_DELETE_AUTHOR
    response = await ac.get(f"/authors/{author_id}")
    assert response.status_code == 404


async def test_create_author_wrong_data(ac: AsyncClient):
    wrong_author_data = {"name": "Иван", "surname": "Иванов", "date_birth": "1924"}
    response = await ac.post("/authors/", json=wrong_author_data)
    assert response.status_code == 422
    wrong_author_data = {"name": "", "surname": "Иванов", "date_birth": "1924-12-18"}
    response = await ac.post("/authors/", json=wrong_author_data)
    assert response.status_code == 422
    wrong_author_data = {"surname": "Иванов", "date_birth": "1924-12-18"}
    response = await ac.post("/authors/", json=wrong_author_data)
    assert response.status_code == 422


async def test_create_get_by_id_author_wrong_data(ac: AsyncClient, author_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    response = await ac.get(f"/authors/{-1000}")
    assert response.status_code == 404


async def test_create_update_author_wrong_data(ac: AsyncClient, author_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    author_update_data = {"name": "Иван", "surname": "Иванов", "date_birth": "-1924-12-18"}
    response = await ac.put(f"/authors/{author_id}", json=author_update_data)
    assert response.status_code == 422


async def test_wrong_delete_author(ac: AsyncClient, author_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    wrong_author_id = 1000
    assert author_id != wrong_author_id
    response = await ac.delete(f"/authors/{wrong_author_id}")
    assert response.status_code == 404
