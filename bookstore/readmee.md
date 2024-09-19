Unit test

# Web Application Test Suite

This repository contains automated tests for a web application using `pytest` and `httpx`. The tests are organized into classes that focus on different aspects of the application, specifically user authentication and book management.

## Structure

The tests are divided into the following classes:

- `TestUserAuthentication`: Contains tests related to user signup and login.
- `TestBookAPI`: Contains tests for book management including creation, retrieval, and deletion of books.
- `TestBookAPIErrorHandling`: Focuses on error handling for book-related operations.



Integration test

# FastAPI Test Suite with Pytest and Mocking

## Overview

This repository contains test cases for a FastAPI application that handles books, written using **Pytest** and **unittest.mock**. The tests cover core CRUD (Create, Read, Update, Delete) functionalities of the API, including edge cases such as handling non-existent resources. We have also implemented JWT authentication mocking to simulate authorized requests during the test cases.

## Key Components

1. **FastAPI TestClient**: We use `TestClient` from FastAPI to simulate API requests within the test environment.
2. **Mocking**: 
   - The **JWTBearer dependency** is mocked to bypass authentication checks and simplify testing.
   - The **SQLAlchemy session** is mocked using `MagicMock` to simulate database interactions without hitting the actual database.
3. **Fixtures**: Pytest fixtures are used for mocking both the JWT and database session, providing reusable and isolated test configurations.
4. **Asynchronous Tests**: Since FastAPI supports asynchronous request handling, we have used `pytest.mark.asyncio` to ensure the tests are asynchronous and compatible with the FastAPI application.

## Explanation of Changes

### 1. **Refactored Variable and Function Names**
   - Renamed the variables and fixtures to make the code more readable and to reflect their functionality better. For example:
     - `mock_jwt_bearer` → `mock_jwt_dependency`
     - `mock_db_session` → `mock_session`
     - `mock_book` → `sample_book`
     - Function names were updated to be more descriptive and aligned with Python naming conventions.

### 2. **Test Cases**

Each test case corresponds to a specific FastAPI endpoint, and here’s a breakdown of the tests included:

- **`test_add_new_book`**: This test checks the `/books/` POST endpoint, ensuring a book can be created successfully. It mocks a book addition operation using a sample book dictionary.
  
- **`test_modify_book`**: Verifies that the book update process works as expected via the `/books/{id}` PUT endpoint. The test checks if the book’s data is updated successfully.

- **`test_remove_book`**: Tests the `/books/{id}` DELETE endpoint, ensuring that the book can be deleted and that the appropriate response is returned.

- **`test_create_then_fetch_book`**: This test performs two actions:
  1. Creates a book.
  2. Fetches the same book using its `id`.
  
- **`test_fetch_nonexistent_book`**: Simulates a scenario where the requested book does not exist and checks whether a 404 error is returned.

- **`test_list_all_books`**: Ensures the `/books/` GET endpoint correctly returns a list of all books in the database.

- **`test_update_nonexistent_book`**: Attempts to update a non-existent book and checks for the appropriate 404 error response.

- **`test_delete_nonexistent_book`**: Similar to the previous test, this checks if deleting a non-existent book returns the correct error.

- **`test_list_books_by_author`**: Tests if books by a specific author can be listed correctly by passing an `author_id` query parameter.

### 3. **Mocking Enhancements**

- **JWT Authentication**: Instead of using the actual JWTBearer middleware for authorization, the test suite mocks this dependency so that all requests are automatically considered authenticated.
  
- **Database Interaction**: All database interactions are mocked using the SQLAlchemy `Session` object. This avoids the need to connect to a real database and speeds up the testing process by working with in-memory mocks.


### 5. **Edge Case Testing**

- The test suite includes scenarios for handling non-existent books (both for fetch, update, and delete operations) to ensure the API responds with appropriate error messages and status codes.

