# Support CRM Backend

A robust REST API backend for a customer support ticketing system built with FastAPI, SQLAlchemy, and SQLite.

## Project Overview

This backend service manages support ticketing system API with CRUD operations for tickets and notes, providing endpoints to search, filter, and update tickets.

## Tech Stack

- **FastAPI** - High-performance web framework
- **SQLite** - Lightweight SQL database
- **SQLAlchemy** - ORM for database interactions
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server for FastAPI

## Setup Instructions

### Prerequisites

- Python 3.9+
- pip

## Installation

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create a virtual environment (recommended)**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running Locally

### Start the Development Server

```bash
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

### API Documentation

FastAPI auto-generates interactive API documentation:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Tickets

| Endpoint                     | Method | Description                                                                 |
|------------------------------|--------|-----------------------------------------------------------------------------|
| `/api/tickets`              | POST   | Create a new ticket                                                          |
| `/api/tickets`              | GET    | List all tickets with search (supports search by ticket ID, customer name, subject, and status filter |
| `/api/tickets/{ticket_id}`  | GET    | Get a single ticket by ID with its ticket_id (including associated notes)   |
| `/api/tickets/{ticket_id}`  | PUT    | Update ticket status and/or add a new note to the ticket                    |

## Database Schema

### Tickets Table (`tickets`)

| Column           | Type         | Description                         |
|-------------------|--------------|---------------------------------|
| id                | Integer      | Primary key (auto-increment)      |
| ticket_id         | String       | Unique ticket identifier (e.g., TCK-1001) |
| customer_name     | String       | Customer's name                  |
| customer_email    | String       | Customer's email                 |
| subject           | String       | Ticket subject                   |
| description       | Text         | Detailed ticket description    |
| status            | String       | Ticket status (Open, In Progress, Closed) |
| created_at        | DateTime     | Ticket creation timestamp      |
| updated_at        | DateTime     | Ticket last update timestamp    |

### Notes Table (`notes`)

| Column           | Type         | Description                         |
|-------------------|--------------|---------------------------------|
| id                | Integer      | Primary key (auto-increment)      |
| ticket_id         | String       | Foreign key to tickets.ticket_id      |
| note_text        | Text         | Note content                    |
| created_at        | DateTime     | Note creation timestamp        |

## Folder Structure

```
backend/
├── app/
│   ├── api/             # API routes (tickets.py)
│   ├── crud/            # Database operations (CRUD functions)
│   ├── models/          # SQLAlchemy database models
│   ├── schemas/         # Pydantic validation schemas
│   ├── __init__.py
│   ├── database.py      # Database connection and session setup
│   └── main.py        # FastAPI application entry point
├── requirements.txt  # Project dependencies
└── .gitignore        # Git ignore file
```

## Deployment URL

- **Railway Deployment**: (Replace with your actual Railway URL after deployment)
- **Other Host**: (Replace with your actual deployment URL after deployment)

## License

This project is for assessment purposes only.
