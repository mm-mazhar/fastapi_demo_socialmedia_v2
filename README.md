# FastAPI Demo Social Media Application

This is a demonstration project of a CRUD-based social media API using **FastAPI**. The application leverages **SQLAlchemy** for database interactions, **Alembic** for migrations, and **JWT** for authentication. It showcases the implementation of modern RESTful API practices, focusing on user authentication, schema validation, and seamless integration with a PostgreSQL database.

## Key Features:

- User Management: Includes user creation, updates, and deletion with proper schema validation using Pydantic.
- Post Management: Implements CRUD operations for posts, enabling a robust social media-like structure.
- Authentication: Utilizes OAuth2 with JWT tokens for secure access control.
- Database Management: Uses SQLAlchemy for ORM operations and Alembic for database migrations.
- Scalability: Written with modularity and scalability in mind, making it a perfect foundation for larger projects.

### Technologies Used:

- FastAPI: For API development with auto-generated OpenAPI documentation.
- PostgreSQL: As the database for storing user and post information.
- Alembic: For managing database schema migrations.
- Pytest: For testing the endpoints and business logic.
- Uvicorn: For serving the FastAPI application.

This repository is a practical example of how to build and structure a FastAPI project with real-world use cases. It is suitable for developers looking to learn FastAPI or use it as a starting point for their projects.v

## Requirements

## Prerequisites

- Python 3.11 or higher
- PostgreSQL
- Docker (optional for containerization)

## Dependencies

Install the required Python packages listed in `Pipfile` using `pipenv`:

```bash
pipenv install
```

## Setup

1. Clone the Repository

```bash
git clone https://github.com/your-repo/fastapi-demo-socialmedia.git
cd fastapi-demo-socialmedia
```

2. Configure Environment Variables

Create a .env file in the root directory with the following variables:

```bash
DB_HOSTNAME=<your_postgres_host>
DB_PORT=5432
DB_NAME=FastAPI-FAA
DB_USERNAME=postgres
DB_PASS=your_password
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

3. Database Setup

Apply database migrations:

```bash
alembic upgrade head
```

4. Run the Application

- Locally:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

- Using Docker:

```bash
docker-compose up --build
```

## API Documentation

Interactive API documentation is available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

or

- Swagger UI: https://fastapi-demo-socialmedia-v2.onrender.com/docs
- ReDoc: https://fastapi-demo-socialmedia-v2.onrender.com//redoc

## Endpoints Overview

#### Users

- POST /users/create-user: Create a new user.
- GET /users/get: Retrieve user(s).
- PUT /users/update/{username}: Update a user's details.
- DELETE /users/delete/{id}: Delete a user by ID.

#### Posts

- POST /posts/create: Create a new post.
- GET /posts/get: Retrieve posts.
- GET /posts/id/{id}: Get a post by ID.
- PUT /posts/update/{id}: Update a post by ID.
- DELETE /posts/delete/{id}: Delete a post by ID.

#### Authentication

- POST /login: User login and token generation.

#### Description

- GET /description: API and project metadata.

## Testing

Run tests using pytest:

```bash
pytest
```
