from httpx import AsyncClient
from .messages import (
    FAILED_CREATE_BOOK,
    FAILED_GET_BOOK,
    FAILED_GET_BOOKS,
    FAILED_UPDATE_BOOK,
    FAILED_DELETE_BOOK,
    FAILED_NUMBER_OF_BOOKS,
    FAILED_CREATE_AUTHOR
)


async def test_create_get_books(ac: AsyncClient, author_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    author_id = response.json()["id"]
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    number_of_books = 11
    for i in range(number_of_books):
        book_data = {
            "name": f"Супер книга_{i}",
            "description": "Интересная",
            "author_id": author_id,
            "quantity": 10
        }
        response = await ac.post("/books/", json=book_data)
        assert response.status_code == 201, FAILED_CREATE_BOOK
    response = await ac.get("/books/?offset=0&limit=10")
    assert response.status_code == 200, FAILED_GET_BOOKS + "offset=0&limit=10"
    assert len(response.json()) == 10, FAILED_NUMBER_OF_BOOKS + "10"
    response = await ac.get("/books/?offset=0&limit=20")
    assert response.status_code == 200, FAILED_GET_BOOKS + "offset=0&limit=20"
    assert len(response.json()) == number_of_books, f"{FAILED_NUMBER_OF_BOOKS} {number_of_books}"
    response = await ac.get("/books/?offset=1&limit=11")
    assert response.status_code == 200, FAILED_GET_BOOKS + "offset=1&limit=11"
    assert len(response.json()) == number_of_books - 1,  f"{FAILED_NUMBER_OF_BOOKS} {number_of_books - 1}"


async def test_create_get_book_by_id(ac: AsyncClient, author_payload: dict, book_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    author_id = response.json()["id"]
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    assert response.status_code == 201, FAILED_CREATE_BOOK
    book_id = response.json()["id"]
    response = await ac.get(f"/books/{book_id}")
    assert response.status_code == 200, FAILED_GET_BOOK
    book_payload["id"] = response.json()["id"]
    #book_payload["order_items"] = []
    #book_payload["author"] = None
    #book_payload["borrows"] = []
    assert book_payload == response.json()


async def test_create_update_book(ac: AsyncClient, author_payload: dict, book_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    assert response.status_code == 201, FAILED_CREATE_BOOK
    book_id = response.json()["id"]
    book_update_data = {
        "name": f"Книга",
        "description": "kk",
        "author_id": author_id,
        "quantity": 5
    }
    response = await ac.put(f"/books/{book_id}", json=book_update_data)
    assert response.status_code == 200, FAILED_UPDATE_BOOK
    book_update_data["id"] = book_id
    assert response.json() == book_update_data


async def test_delete_book(ac: AsyncClient, author_payload: dict, book_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    assert response.status_code == 201, FAILED_CREATE_BOOK
    book_id = response.json()["id"]
    response = await ac.delete(f"/books/{book_id}")
    assert response.status_code == 204, FAILED_DELETE_BOOK
    response = await ac.get(f"/books/{book_id}")
    assert response.status_code == 404


async def test_create_book_wrong_data(ac: AsyncClient, author_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    wrong_book_data = {
        "name": "Супер книга",
        "description": "Интересная",
        "author_id": author_id,
        "quantity": -10
    }
    response = await ac.post("/books/", json=wrong_book_data)
    assert response.status_code == 422
    wrong_book_data = {
        "name": "",
        "description": "Интересная",
        "author_id": author_id,
        "quantity": 10
    }
    response = await ac.post("/books/", json=wrong_book_data)
    assert response.status_code == 422
    wrong_book_data = {
        "description": "Интересная",
        "author_id": author_id,
        "quantity": -10
    }
    response = await ac.post("/books/", json=wrong_book_data)
    assert response.status_code == 422


async def test_create_get_by_id_book_wrong_data(ac: AsyncClient, author_payload: dict, book_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    assert response.status_code == 201, FAILED_CREATE_BOOK
    response = await ac.get(f"/books/{-1007}")
    assert response.status_code == 404


async def test_create_update_book_wrong_data(ac: AsyncClient, author_payload: dict, book_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    assert response.status_code == 201, FAILED_CREATE_BOOK
    book_id = response.json()["id"]
    book_update_data = {
        "name": "Умная книга",
        "description": "Впечатляет",
        "author_id": author_id
    }
    response = await ac.put(f"/books/{book_id}", json=book_update_data)
    assert response.status_code == 422


async def test_wrong_delete_book(ac: AsyncClient, author_payload: dict, book_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    #вот так сделать!
    #author_id = get_author_id(ac, author_payload)
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    assert response.status_code == 201, FAILED_CREATE_BOOK
    book_id = response.json()["id"]
    wrong_book_id = 1000
    assert book_id != wrong_book_id
    response = await ac.delete(f"/books/{wrong_book_id}")
    assert response.status_code == 404

"""
async def get_author_id(ac: AsyncClient, author_payload: dict) -> int:
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    return author_id
"""