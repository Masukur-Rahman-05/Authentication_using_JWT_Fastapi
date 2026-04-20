# JWT Authentication with FastAPI

A simple FastAPI project that implements JWT-based authentication with PostgreSQL and SQLAlchemy. Users can sign up, log in to receive an access token, and access protected endpoints with a Bearer token.

## Features

- User registration with hashed passwords
- JWT token generation and verification
- Protected profile endpoint
- Protected endpoint to list all users
- PostgreSQL database integration with SQLAlchemy

## Tech Stack

- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Pydantic
- `python-jose` for JWT handling
- `passlib` and `bcrypt` for password hashing

## Project Structure

```text
Authentication_using_jwt/
|-- app/
|   |-- auth.py
|   |-- database.py
|   |-- main.py
|   |-- models.py
|   |-- schemas.py
|   `-- __init__.py
|-- .env
|-- docker-compose.yml
|-- requirements.txt
`-- README.md
```

## Environment Variables

Create a `.env` file in the project root with these keys:

```env
APP_NAME=JWT Auth API
DATABASE_URL=postgresql://username:password@localhost:5432/db_name
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Installation

1. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Make sure PostgreSQL is running and `DATABASE_URL` points to a valid database.

## Database Setup

This project defines the `users` table model, but it does not currently include an automatic table creation step or Alembic migration files in the repository.

Before using the API, create the database table by either:

- adding a startup/init script that runs `Base.metadata.create_all(bind=engine)`, or
- creating and applying Alembic migrations, or
- creating the `users` table manually in PostgreSQL.

## Run the Application

```powershell
uvicorn app.main:app --reload
```

After startup, the API will usually be available at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### `POST /signup`

Create a new user.

Request body:

```json
{
  "email": "user@example.com",
  "username": "user123",
  "password": "strongpassword"
}
```

### `POST /login`

Authenticate a user and return a JWT access token.

This endpoint expects form data, not JSON.

Example form fields:

```text
username=user123
password=strongpassword
```

Example response:

```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer"
}
```

### `GET /profile`

Return the currently authenticated user.

Header:

```text
Authorization: Bearer <your-jwt-token>
```

### `GET /users`

Return all users. This route is also protected by JWT authentication.

## Example Workflow

1. Sign up a user with `POST /signup`
2. Log in with `POST /login`
3. Copy the returned token
4. Call `GET /profile` or `GET /users` with `Authorization: Bearer <token>`

## Notes

- Passwords are stored as hashes, not plain text.
- JWT payloads use the user's email as the `sub` claim.
- The login endpoint looks up users by `username`.
- `docker-compose.yml` exists in the repo but is currently empty.

## License

Add a license here if you plan to distribute the project.
