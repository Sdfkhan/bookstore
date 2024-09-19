import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app  # Assuming the FastAPI app is in the main module
from database import get_db, Book  # Assuming Book and get_db are imported from the database module

# Initializing TestClient for interacting with FastAPI endpoints
client = TestClient(app)

# Mock book data
sample_book = Book(id=1, name="Sample Book", author="Sample Author", published_year=2023, book_summary="Sample Summary")
sample_books_list = [sample_book]


# Mock JWT dependency for testing purposes
@pytest.fixture
def mock_jwt_dependency():
    with patch("middleware.JWTBearer.__call__", return_value=True):
        yield


# Mocking the database session for SQLAlchemy interactions
@pytest.fixture
def mock_session():
    fake_session = MagicMock(spec=Session)
    fake_session.add.return_value = None
    fake_session.commit.return_value = None
    fake_session.refresh.side_effect = lambda x: x  # Simulates returning the object post-refresh
    with patch("database.get_db", return_value=fake_session):
        yield fake_session


# Simulate database queries to test API interactions
@pytest.fixture
def mock_query():
    fake_query = MagicMock()
    fake_query.filter.return_value.first.return_value = sample_book
    fake_query.all.return_value = sample_books_list
    return fake_query


# Test case for creating a book using POST method
@pytest.mark.asyncio
async def test_add_new_book(mock_jwt_dependency, mock_session, mock_query):
    new_book = sample_book.dict()
    response = client.post("/books/", json=new_book)
    assert response.status_code == 200
    assert response.json() == new_book


# Test case for updating a book's information using PUT method
@pytest.mark.asyncio
async def test_modify_book(mock_jwt_dependency, mock_session, mock_query):
    book_updates = {"name": "Updated Title"}
    response = client.put("/books/1", json=book_updates)
    assert response.status_code == 200
    expected_result = sample_book.dict()
    expected_result.update(book_updates)
    assert response.json() == expected_result


# Test case for deleting a book using DELETE method
@pytest.mark.asyncio
async def test_remove_book(mock_jwt_dependency, mock_session, mock_query):
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book successfully removed"}


# Combined test for creating a book and then retrieving it by its ID
@pytest.mark.asyncio
async def test_create_then_fetch_book(mock_jwt_dependency, mock_session, mock_query):
    # Adding the book
    post_response = client.post("/books/", json=sample_book.dict())
    assert post_response.status_code == 200
    new_book = post_response.json()

    # Fetching the newly added book by its ID
    get_response = client.get(f"/books/{new_book['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == new_book


# Test for retrieving books by a specific author
@pytest.mark.asyncio
async def test_list_books_by_author(mock_jwt_dependency, mock_session, mock_query):
    mock_query.filter_by.return_value.all.return_value = sample_books_list
    response = client.get("/books/?author_id=1")
    assert response.status_code == 200
    assert response.json() == [book.dict() for book in sample_books_list]


# Test for attempting to fetch a non-existent book
@pytest.mark.asyncio
async def test_fetch_nonexistent_book(mock_jwt_dependency, mock_session, mock_query):
    mock_query.filter.return_value.first.return_value = None
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


# Test for listing all available books
@pytest.mark.asyncio
async def test_list_all_books(mock_jwt_dependency, mock_session, mock_query):
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json() == [book.dict() for book in sample_books_list]


# Test for updating a non-existent book entry
@pytest.mark.asyncio
async def test_update_nonexistent_book(mock_jwt_dependency, mock_session, mock_query):
    mock_query.filter.return_value.first.return_value = None
    update_data = {"name": "Non-existent Book"}
    response = client.put("/books/999", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


# Test for deleting a non-existent book entry
@pytest.mark.asyncio
async def test_delete_nonexistent_book(mock_jwt_dependency, mock_session, mock_query):
    mock_query.filter.return_value.first.return_value = None
    response = client.delete("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}
