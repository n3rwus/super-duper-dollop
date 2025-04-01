# Social Media Backend API (FastAPI + MySQL)

This is a backend API for a social media application built with **FastAPI**, following the **MVC (Model-View-Controller) design pattern**. It includes authentication, post management, caching, and database interactions using **MySQL** and **SQLAlchemy ORM**.

## Features

- **Authentication**: JWT-based token authentication
- **User Management**: Signup & login with secure password hashing (bcrypt)
- **Post Management**: Add, retrieve, and delete posts
- **Data Validation**: Using **Pydantic** for strict input validation
- **Caching**: In-memory caching for efficient API responses
- **Dependency Injection**: For authentication and request validation
- **ORM Integration**: Using **SQLAlchemy** for MySQL operations
- **Docker Support**: Run in a containerized development environment

---

## Project Structure

```
project_root/
│
├── .env                               # Environment variables file
├── requirements.txt                   # Project dependencies
│
└── app/                               # Main application package
    ├── main.py                        # Application entry point
    │
    ├── core/                          # Core functionality
    │   ├── __init__.py
    │   ├── auth.py                    # Authentication dependencies
    │   ├── cache.py                   # Caching implementation
    │   ├── config.py                   # App configuration
    │   └── security.py                 # Password hashing and JWT functions
    │
    ├── db/                            # Database related code
    │   ├── __init__.py
    │   └── database.py                 # Database connection setup
    │
    ├── models/                        # Data models
    │   ├── __init__.py
    │   └── models.py                   # SQLAlchemy models
    │
    ├── repositories/                  # Data access layer
    │   ├── __init__.py
    │   ├── user_repository.py          # User database operations
    │   └── post_repository.py          # Post database operations
    │
    ├── routes/                        # API endpoints
    │   ├── __init__.py
    │   ├── user.py                     # User authentication routes
    │   └── post.py                     # Post management routes
    │
    ├── schemas/                       # Pydantic models
    │   ├── __init__.py
    │   └── schemas.py                   # Request/response validation schemas
    │
    └── services/                      # Business logic layer
        ├── __init__.py
        ├── user_service.py             # User-related business logic
        └── post_service.py             # Post-related business logic
```

---

## Setup Instructions

### 1. Create a Virtual Environment

```bash
cd project_root
python -m venv venv
```

Activate the virtual environment:

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```ini
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_NAME=social_api
SECRET_KEY=your-secret-key-at-least-32-characters-long
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000/`

---

## Running with Docker (Recommended for Development)

### 1. Build and Start the Containers

```bash
docker-compose up --build
```

### 2. Access the API

- **API Base URL**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Database Management (Adminer)**: [http://localhost:8080](http://localhost:8080)
  
Use the following credentials in **Adminer**:
  - System: **MySQL**
  - Server: **db**
  - Username: **social_user**
  - Password: **social_password**
  - Database: **social_api**

### 3. Stop the Containers

```bash
docker-compose down
```

To remove the database volume:

```bash
docker-compose down -v
```

---

## API Endpoints

### 1. Authentication

- **Signup**: `POST /signup`
- **Login**: `POST /login`
  - Returns a JWT token

### 2. Post Management

- **Add Post**: `POST /post`
  - Requires authentication (token in header)
  - Validates payload size (max 1MB)
  
- **Get Posts**: `GET /posts`
  - Requires authentication
  - Uses caching (5-minute expiration)
  
- **Delete Post**: `DELETE /post/{post_id}`
  - Requires authentication

---

## Troubleshooting

### 1. Database Connection Issues

If the application fails to connect to MySQL, check:
- MySQL is running (`docker-compose up` or start MySQL manually)
- Your `.env` file has correct credentials
- If using SQLite, update `app/db/database.py` to use SQLite instead of MySQL.

### 2. Pydantic v2 Migration Issues

Update all occurrences of:

```python
class Config:
    orm_mode = True
```

To:

```python
class Config:
    from_attributes = True
```

If not installed, run:

```bash
pip install pydantic-settings
```

---

## Future Improvements

- **Rate Limiting**: Prevent abuse with request rate limiting
- **Unit Tests**: Implement testing with **pytest**
- **Logging**: Add structured logging with `loguru`
- **CI/CD**: Automate deployment with GitHub Actions

---

## License

This project is licensed under the MIT License.

