Set up

repo/
│── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py          # User authentication (login, register, JWT, OAuth)
│   │   │   ├── files.py         # Upload, retrieve user files
│   │   │   ├── rag.py           # LLM query processing for user files
│   │   │   ├── __init__.py
│   │   ├── dependencies.py      # Common dependencies (DB, auth middleware)
│   ├── core/
│   │   ├── config.py            # App settings (env variables, database URL)
│   │   ├── security.py          # Password hashing, JWT handling
│   ├── models/
│   │   ├── user.py              # User model (id, email, hashed_password)
│   │   ├── file.py              # File model (id, user_id, storage_path)
│   │   ├── __init__.py
│   ├── schemas/
│   │   ├── user.py              # Pydantic models for user auth
│   │   ├── file.py              # Pydantic models for file management
│   │   ├── rag.py               # Request/response schemas for LLM queries
│   │   ├── __init__.py
│   ├── services/
│   │   ├── file_service.py      # S3/GCS integration for file storage
│   │   ├── rag_service.py       # Calls OpenAI API for RAG
│   │   ├── auth_service.py      # User authentication logic
│   │   ├── __init__.py
│   ├── main.py                  # Entry point for FastAPI app
│── migrations/                   # Alembic database migrations
│── tests/
│   ├── test_auth.py
│   ├── test_files.py
│   ├── test_rag.py
│── .env                           # Environment variables
│── requirements.txt               # Python dependencies
│── Dockerfile                     # Containerization setup
│── docker-compose.yml              # Optional, for local development
│── alembic.ini                     # Alembic migration config
│── README.md                       # Project documentation
