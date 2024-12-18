import asyncio
from httpx import AsyncClient
from .messages import (
    FAILED_CREATE_BORROW,
    FAILED_GET_BORROW,
    FAILED_GET_BORROWS,
    FAILED_UPDATE_BORROW,
    FAILED_CREATE_BOOK,
    FAILED_GET_BOOK,
    FAILED_CREATE_AUTHOR
)


async def create_borrow(ac: AsyncClient, borrow_data: dict):
    return await ac.post("/borrows/", json=borrow_data)


async def test_create_get_borrows(ac: AsyncClient, author_payload: dict, book_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    book_id = response.json()["id"]
    assert response.status_code == 201, FAILED_CREATE_BOOK
    # create borrows
    borrows_data = [
        {"book_id": book_id, "reader_name": "Вася1"},
        {"book_id": book_id, "reader_name": "Вася2"},
        {"book_id": book_id, "reader_name": "Вася3"}
    ]
    tasks = [create_borrow(ac, borrow_data) for borrow_data in borrows_data]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        assert response.status_code == 201, FAILED_CREATE_BORROW
    response = await ac.get(f"/books/{book_id}")
    assert response.status_code == 200, FAILED_GET_BOOK
    assert response.json()["quantity"] == 7, "Неправильное оставшееся кол-во книг"  # 10-3=7
    # get borrows
    response = await ac.get("/borrows/?offset=0&limit=20")
    assert response.status_code == 200, FAILED_GET_BORROWS + "offset=0&limit=20"
    assert len(response.json()) == len(borrows_data)
    response = await ac.get("/borrows/?offset=0&limit=2")
    assert response.status_code == 200, FAILED_GET_BORROWS + "offset=0&limit=2"
    assert len(response.json()) == 2
    response = await ac.get("/borrows/?offset=1&limit=20")
    assert response.status_code == 200, FAILED_GET_BORROWS + "offset=1&limit=20"
    assert len(response.json()) == len(borrows_data) - 1


async def test_create_get_borrow_by_id(
        ac: AsyncClient,
        author_payload: dict,
        book_payload: dict,
        borrow_payload: dict
):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    assert response.status_code == 201, FAILED_CREATE_BOOK
    book_id = response.json()["id"]
    borrow_payload["book_id"] = book_id
    response = await ac.post("/borrows/", json=borrow_payload)
    assert response.status_code == 201, FAILED_CREATE_BORROW
    borrow_id = response.json()["id"]
    response = await ac.get(f"/borrows/{borrow_id}")
    assert response.status_code == 200, FAILED_GET_BORROW
    borrow_payload["id"] = response.json()["id"]
    borrow_payload["borrow_date"] = response.json()["borrow_date"]
    borrow_payload["book"] = response.json()["book"]
    assert borrow_payload == response.json()


async def test_create_update_borrow_return_date(
        ac: AsyncClient,
        author_payload: dict,
        book_payload: dict,
        borrow_payload: dict
):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    assert response.status_code == 201, FAILED_CREATE_BOOK
    book_id = response.json()["id"]
    borrow_payload["book_id"] = book_id
    response = await ac.post("/borrows/", json=borrow_payload)
    assert response.status_code == 201, FAILED_CREATE_BORROW
    borrow_id = response.json()["id"]
    response = await ac.get(f"/borrows/{borrow_id}")
    assert response.status_code == 200, FAILED_GET_BORROW
    borrow_return_date = {"return_date": "2024-12-18"}
    response = await ac.patch(f"/borrows/{borrow_id}", json=borrow_return_date)
    assert response.status_code == 200, FAILED_UPDATE_BORROW
    assert response.json()["return_date"] == borrow_return_date["return_date"], "Дата возврата обновилась некорректно"


async def test_create_borrow_wrong_data(ac: AsyncClient, author_payload: dict, book_payload: dict):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    assert response.status_code == 201, FAILED_CREATE_BOOK
    book_id = response.json()["id"]
    wrong_borrow_data = {
        "book_id": 100,
        "reader_name": "Вася"
    }
    response = await ac.post("/borrows/", json=wrong_borrow_data)
    assert response.status_code == 400
    wrong_borrow_data = {
        "reader_name": "Вася"
    }
    response = await ac.post("/borrows/", json=wrong_borrow_data)
    assert response.status_code == 422

    wrong_borrow_data = {
        "book_id": book_id,
        "reader_name": 123
    }
    response = await ac.post("/borrows/", json=wrong_borrow_data)
    assert response.status_code == 422


async def test_create_get_by_id_borrow_wrong_data(
        ac: AsyncClient,
        author_payload: dict,
        book_payload: dict,
        borrow_payload: dict
):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    assert response.status_code == 201, FAILED_CREATE_BOOK
    book_id = response.json()["id"]
    borrow_payload["book_id"] = book_id
    response = await ac.post("/borrows/", json=borrow_payload)
    assert response.status_code == 201, FAILED_CREATE_BORROW
    borrow_id = response.json()["id"]
    wrong_borrow_id = 100
    assert wrong_borrow_id != borrow_id
    response = await ac.get(f"/borrows/{wrong_borrow_id}")
    assert response.status_code == 404


async def test_create_update_borrow_return_date_wrong_data(
        ac: AsyncClient,
        author_payload: dict,
        book_payload: dict,
        borrow_payload: dict
):
    response = await ac.post("/authors/", json=author_payload)
    assert response.status_code == 201, FAILED_CREATE_AUTHOR
    author_id = response.json()["id"]
    book_payload["author_id"] = author_id
    response = await ac.post("/books/", json=book_payload)
    assert response.status_code == 201, FAILED_CREATE_BOOK
    book_id = response.json()["id"]
    borrow_payload["book_id"] = book_id
    response = await ac.post("/borrows/", json=borrow_payload)
    assert response.status_code == 201, FAILED_CREATE_BORROW
    borrow_id = response.json()["id"]
    wrong_borrow_update_data = {"return_date": "aaa"}
    response = await ac.patch(f"/borrows/{borrow_id}", json=wrong_borrow_update_data)
    assert response.status_code == 422
