# Guest Relations Management System

A comprehensive web application for managing guest relations cases, PDF processing, and AI-powered email responses using RAG (Retrieval-Augmented Generation) technology.

## Features

- **Case Management**: Create, track, and manage guest relations cases
- **PDF Processing**: Upload and process PDF documents with AI analysis
- **AI Email Assistant**: Generate professional email responses using RAG technology
- **Task Management**: Assign and track daily tasks for staff
- **Follow-up System**: Manage follow-up actions and communications
- **User Authentication**: Secure login system with role-based access
- **Real-time Updates**: Live updates for case status and task assignments

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **MySQL**: Primary database
- **Alembic**: Database migrations
- **OpenAI API**: AI-powered text generation
- **JWT**: Authentication tokens
- **Uvicorn**: ASGI server

### Frontend
- **React 19**: Modern React with hooks
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and dev server

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- OpenAI API key

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GR_Domes
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   # Create database
   mysql -u root -p
   CREATE DATABASE mydb;
   
   # Run migrations
   alembic upgrade head
   
   # Seed initial data
   python seed_users.py
   ```

4. **Environment Configuration**
   ```bash
   # Create .env file in backend directory
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

6. **Run the application**
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn main:app --reload
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

## Production Deployment

### Using Docker (Recommended)

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Access the application**
   - Frontend: http://localhost
   - API: http://localhost/api
   - API Docs: http://localhost/docs (development only)

### Manual Production Setup

1. **Backend Production**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Frontend Production**
   ```bash
   cd frontend
   npm run build
   # Serve the dist folder with a web server like nginx
   ```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-openai-api-key-here
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
ENVIRONMENT=production
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
GR_Domes/
├── backend/
│   ├── alembic/           # Database migrations
│   ├── routers/           # API route handlers
│   ├── schemas/           # Pydantic models
│   ├── services/          # Business logic
│   ├── training_documents/ # RAG training data
│   ├── uploads/           # File uploads
│   ├── main.py           # FastAPI application
│   ├── models.py         # SQLAlchemy models
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   └── App.jsx       # Main app component
│   ├── package.json      # Node dependencies
│   └── vite.config.js    # Vite configuration
├── docker-compose.yml    # Docker services
├── Dockerfile           # Container configuration
└── nginx.conf           # Nginx configuration
```

## Key Features

### Email AI Assistant
- Paste guest emails and get AI-generated responses
- Uses RAG technology with training documents
- Conversation-like interface with message history
- Copy responses for use in actual emails

### Case Management
- Create and track guest relations cases
- Assign cases to staff members
- Update case status and add notes
- Generate AI feedback for case analysis

### Task Management
- Create daily tasks (Amenity List, Emails, Courtesy Calls)
- Assign tasks to specific users
- Track task completion status
- Admin controls for task management

### PDF Processing
- Upload PDF documents for analysis
- Extract text and generate AI insights
- Create cases from PDF content
- Automated workflow processing

## Security Features

- JWT-based authentication
- Role-based access control
- CORS protection
- Input validation
- SQL injection prevention
- XSS protection headers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.
