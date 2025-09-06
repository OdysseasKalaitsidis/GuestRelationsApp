# Guest Relations API Backend

A production-ready FastAPI backend for managing guest relations cases with AI-powered document processing.

## Architecture

```
backend/
├── main.py                 # FastAPI application entry point
├── models.py               # SQLAlchemy database models
├── db.py                   # Database connection and session management
├── requirements.txt        # Python dependencies
├── alembic.ini            # Database migration configuration
├── routers/               # API route handlers
│   ├── auth_route.py      # Authentication & authorization
│   ├── user_router.py     # User management
│   ├── case_router.py     # Case CRUD operations
│   ├── document_router.py # Document processing
│   ├── followup_router.py # Followup management
│   └── anonymization_router.py # Data anonymization
├── services/              # Business logic layer
│   ├── ai_service.py      # AI-powered suggestions
│   ├── case_service.py    # Case business logic
│   ├── document_service.py # Document processing
│   ├── followup_service.py # Followup business logic
│   ├── user_service.py    # User business logic
│   ├── anonymization_service.py # Data anonymization
│   └── security.py        # Security utilities
└── schemas/               # Pydantic models for API
    ├── case.py            # Case data models
    ├── followup.py        # Followup data models
    └── user.py            # User data models
```

## Core Features

- **Document Processing**: PDF/DOCX upload and AI-powered parsing
- **Case Management**: Full CRUD operations with templates
- **AI Integration**: Smart suggestions and document analysis
- **Security**: JWT authentication with role-based access
- **Database**: SQLAlchemy ORM with Alembic migrations

## Quick Start

### Prerequisites
- Python 3.11
- Supabase PostgreSQL database
- OpenAI API key

### Installation
```bash
pip install -r requirements.txt

# Copy environment template
cp env.example .env
# Edit .env with your actual values

# Setup database
alembic upgrade head

# Run development server
python main.py
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration

### Cases
- `GET /api/cases` - List all cases
- `POST /api/cases` - Create new case
- `GET /api/cases/{id}` - Get case details
- `PUT /api/cases/{id}` - Update case
- `DELETE /api/cases/{id}` - Delete case

### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents/{id}` - Get document details

### Followups
- `GET /api/followups` - List followups
- `POST /api/followups` - Create followup
- `PUT /api/followups/{id}` - Update followup

## Environment Variables

Copy `env.example` to `.env` and configure:

```env
DATABASE_URL=your_supabase_database_url
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_jwt_secret_key
ENVIRONMENT=development
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

## Development

- Interactive API docs available at `/docs`
- Follow PEP 8 coding standards
- Use type hints throughout
- Implement proper error handling
