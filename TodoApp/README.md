# TodoApp

## Description

TodoApp is a web application that allows users to manage their to-do lists. It provides functionality to add, update, delete, and view todos.

## Features

- **Admin Routes:**
  - `/admin/all/todo`: Get all todos in the system (accessible only by admin).
  - `/admin/all/users`: Get all users in the system (accessible only by admin).

## Installation

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the application using `uvicorn main:app --reload`.

## Usage

1. Access the application at `http://localhost:8000`.
2. Use the provided routes to interact with the todos.

## Routes

- **Admin Routes:**
  - `/admin/all/todo`: GET - Get all todos in the system.
  - `/admin/all/users`: GET - Get all users in the system.
- **Todo Routes:**
  - `/todo`: GET - Get all todos belonging to a signed in user
  - `/todo`: POST - Post a todo belonging to a signed in user

## Dependencies

- FastAPI: Web framework for building APIs.
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library.

<!-- ## Middleware

- `admin_dependency`: Middleware for authorizing admin access to specific routes.
- `db_dependency`: Middleware for handling database connections. -->

## Contributors

- [Solomon Ndifereke](https://github.com/DR-FREKE)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
