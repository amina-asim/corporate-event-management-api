# Corporate Event Management API

A RESTful API built with **FastAPI** and **PostgreSQL** to manage corporate events and employee registrations.

## Features

- Create, view, update, and delete corporate events.
- Register employees for events.
- View registrations for a specific event.
- Delete employee registrations.
- Prevent duplicate employee registrations for the same event.
- Enforce event registration capacity.
- Validate incoming data using Pydantic.
- Return appropriate HTTP status codes.
- Interactive API documentation through Swagger UI.
- Automated API tests using Pytest.

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest
- Uvicorn

## Project Structure

```text
corporate-event-management-api/
│
├── tests/
│   └── test_events.py
│
├── .env
├── .gitignore
├── db.py
├── main.py
├── models.py
├── schemas.py
├── services.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd corporate-event-management-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Create a database named:

```sql
CREATE DATABASE corporate_event_management;
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
DB_HOST=localhost
DB_PORT=5432
DB_NAME=corporate_event_management
```

Replace `YOUR_POSTGRES_PASSWORD` with your local PostgreSQL password.

### 6. Create database tables

Run the following command from the project directory:

```bash
python -c "from db import engine, Base; import models; Base.metadata.create_all(bind=engine); print('Database tables created successfully!')"
```

### 7. Start the API

```bash
python -m uvicorn main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

## API Documentation

Open Swagger UI in your browser:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/events` | Create an event |
| GET | `/events` | View all events |
| GET | `/events/{event_id}` | View one event |
| PUT | `/events/{event_id}` | Update an event |
| DELETE | `/events/{event_id}` | Delete an event |
| POST | `/events/{event_id}/registrations` | Register an employee |
| GET | `/events/{event_id}/registrations` | View event registrations |
| DELETE | `/registrations/{registration_id}` | Delete a registration |

## Business Rules

- Event titles and required fields cannot be empty.
- Event capacity must be greater than zero.
- An employee cannot register more than once for the same event.
- An event cannot accept registrations beyond its maximum capacity.
- Employees cannot register for non-existent events.

## HTTP Status Codes

| Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 204 | Resource deleted successfully |
| 404 | Resource not found |
| 409 | Duplicate registration or event capacity reached |
| 422 | Request validation failed |

## Running Automated Tests

Run all tests using:

```bash
python -m pytest -v
```

The automated test suite covers event creation, retrieval, updating, deletion, validation, employee registration, duplicate prevention, capacity limits, and registration retrieval/deletion.

## Security

Database credentials are stored in environment variables rather than hardcoded in the source code. The `.env` file should not be committed to GitHub.

## Author

Developed as a Corporate Event Management API project.