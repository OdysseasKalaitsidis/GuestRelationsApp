# Guest Relations API Backend

A clean, production-ready FastAPI backend for managing guest relations cases, document processing, and AI-powered workflows.

## Architecture Overview

The backend follows a clean, modular architecture with clear separation of concerns:

```
backend/
├── main.py                 # FastAPI application entry point
├── models.py               # SQLAlchemy database models
├── db.py                   # Database connection and session management
├── logging_config.py       # Logging configuration
├── requirements.txt        # Python dependencies
├── alembic.ini            # Database migration configuration
├── routers/               # API route handlers
│   ├── auth_route.py      # Authentication & authorization
│   ├── user_router.py     # User management
│   ├── case_router.py     # Case CRUD + manual input + templates
│   ├── document_router.py # Document processing + workflow
│   ├── followup_router.py # Followup management
│   ├── task_router.py     # Task management
│   └── anonymization_router.py # Data anonymization
├── services/              # Business logic layer
│   ├── ai_service.py      # AI-powered suggestions
│   ├── case_service.py    # Case business logic
│   ├── document_service.py # Document processing
│   ├── case_parser_service.py # Case extraction from documents
│   ├── followup_service.py # Followup business logic
│   ├── task_service.py    # Task business logic
│   ├── user_service.py    # User business logic
│   ├── anonymization_service.py # Data anonymization
│   ├── daily_service.py   # Daily operations
│   └── security.py        # Security utilities
└── schemas/               # Pydantic models for API
    ├── case.py            # Case data models
    ├── followup.py        # Followup data models
    ├── task.py            # Task data models
    └── user.py            # User data models
```

## Core Features

### 1. Document Processing
- **PDF & DOCX Support**: Upload and process various document formats
- **AI-Powered Parsing**: Extract case information using advanced NLP
- **Workflow Automation**: Complete pipeline from document to database

### 2. Case Management
- **CRUD Operations**: Full case lifecycle management
- **Manual Input**: Create cases when documents don't contain sufficient data
- **Templates**: Predefined case templates for common scenarios
- **Bulk Operations**: Handle multiple cases efficiently

### 3. AI Integration
- **Smart Suggestions**: AI-powered feedback for case management
- **Document Analysis**: Intelligent parsing of unstructured documents
- **Workflow Optimization**: Automated case creation and followup generation

### 4. Security & Privacy
- **Authentication**: JWT-based user authentication
- **Authorization**: Role-based access control
- **Data Anonymization**: GDPR-compliant data handling
- **Audit Logging**: Comprehensive activity tracking

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration

### Documents
- `POST /api/documents/upload` - Upload and process documents
- `POST /api/documents/workflow` - Complete workflow automation

### Cases
- `GET /api/cases/` - List all cases
- `POST /api/cases/` - Create single case
- `POST /api/cases/bulk` - Create multiple cases
- `POST /api/cases/manual` - Manual case creation
- `POST /api/cases/template/{name}` - Case from template

### Followups
- `GET /api/followups/` - List followups
- `POST /api/followups/` - Create followup

### Tasks
- `GET /api/tasks/` - List tasks
- `POST /api/tasks/` - Create task

## Getting Started

### Prerequisites
- Python 3.8+
- Supabase PostgreSQL database
- OpenAI API key (for AI features)

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file with:
```env
# Supabase Database Configuration
DATABASE_URL=your_supabase_postgresql_url

# Application Configuration
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your_secret_key
ENVIRONMENT=development
```

### Database Setup
```bash
alembic upgrade head
```

### Running the Application
```bash
python main.py
```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

## Development Guidelines

### Code Quality
- **Type Hints**: All functions use Python type hints
- **Documentation**: Comprehensive docstrings for all endpoints
- **Error Handling**: Consistent error responses with proper HTTP status codes
- **Validation**: Pydantic models for request/response validation

### Testing
- Unit tests for services
- Integration tests for API endpoints
- Database migration testing

### Security
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Rate limiting (production)

## Production Deployment

### Railway/Render Deployment
The application is configured for Railway deployment with:
- Environment-based configuration
- CORS settings for production
- Trusted host middleware
- Static file serving

### Monitoring
- Structured logging
- Health check endpoints
- Performance metrics
- Error tracking

## Contributing

1. Follow the existing code structure
2. Add comprehensive tests
3. Update documentation
4. Use conventional commit messages
5. Ensure all tests pass before submitting

## License

This project is licensed under the MIT License.
