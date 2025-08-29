# Guest Relations Management System

A comprehensive, production-ready system for managing guest relations cases, document processing, and AI-powered workflows. Built with FastAPI backend and React frontend.

## 🏗️ Architecture Overview

The system follows a clean, modular architecture with clear separation of concerns:

```
GR_Domes/
├── backend/                    # FastAPI backend API
│   ├── main.py                # Application entry point
│   ├── models.py               # Database models
│   ├── db.py                   # Database connection
│   ├── requirements.txt        # Python dependencies
│   ├── routers/                # API route handlers (7 routers)
│   ├── services/               # Business logic layer (10 services)
│   ├── schemas/                # Pydantic data models
│   └── alembic/                # Database migrations
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # Page components (3 pages)
│   │   └── services/           # API service layer
│   ├── package.json            # Node.js dependencies
│   └── README.md               # Frontend documentation
├── railway.json                # Railway deployment config
└── README.md                   # This file
```

## 🚀 Core Features

### Backend (FastAPI)
- **Document Processing**: PDF/DOCX upload and AI-powered parsing
- **Case Management**: Full CRUD operations with manual input and templates
- **Workflow Automation**: Complete pipeline from document to database
- **AI Integration**: Smart suggestions and document analysis
- **Security**: JWT authentication, role-based access, data anonymization
- **Database**: SQLAlchemy ORM with Alembic migrations

### Frontend (React)
- **Modern UI**: Clean, responsive interface with Tailwind CSS
- **Document Workflow**: Multi-step upload and processing
- **Case Management**: Comprehensive data tables and forms
- **Real-time Updates**: Live data synchronization
- **Mobile-First**: Responsive design for all devices

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: SQLAlchemy 2.0+ with MySQL/PostgreSQL
- **AI**: OpenAI integration for document analysis
- **Authentication**: JWT with bcrypt
- **Document Processing**: PyPDF2, python-docx, spaCy
- **Deployment**: Railway-ready with environment config

### Frontend
- **Framework**: React 18 with Hooks
- **Build Tool**: Vite for fast development
- **Styling**: Tailwind CSS utility framework
- **Routing**: React Router for navigation
- **HTTP**: Fetch API with centralized service layer

## 📋 Prerequisites

- **Python 3.8+** for backend
- **Node.js 16+** for frontend
- **MySQL/PostgreSQL** database
- **OpenAI API key** for AI features
- **Railway account** for deployment (optional)

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=your_database_url
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your_secret_key
ENVIRONMENT=development" > .env

# Setup database
alembic upgrade head

# Run development server
python main.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000/api" > .env

# Start development server
npm run dev
```

### 3. Access the System
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=mysql://user:pass@localhost/guest_relations
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key_here
ENVIRONMENT=development
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
```

### Database Configuration
The system supports both MySQL and PostgreSQL. Update `backend/db.py` and `backend/alembic.ini` for your database choice.

## 📚 API Documentation

### Core Endpoints

#### Authentication
- `POST /api/auth/login` - User authentication
- `POST /api/auth/register` - User registration

#### Documents
- `POST /api/documents/upload` - Upload and process documents
- `POST /api/documents/workflow` - Complete workflow automation

#### Cases
- `GET /api/cases/` - List all cases
- `POST /api/cases/` - Create single case
- `POST /api/cases/bulk` - Create multiple cases
- `POST /api/cases/manual` - Manual case creation
- `POST /api/cases/template/{name}` - Case from template

#### Followups & Tasks
- `GET /api/followups/` - List followups
- `GET /api/tasks/` - List tasks

### Interactive API Docs
Visit `/docs` when running the backend for interactive Swagger documentation.

## 🏭 Production Deployment

### Railway Deployment
The system is pre-configured for Railway deployment:

1. **Connect Repository**: Link your GitHub repository to Railway
2. **Environment Variables**: Set production environment variables
3. **Auto-Deploy**: Railway automatically builds and deploys on push

### Environment Configuration
```env
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com
RAILWAY_PUBLIC_DOMAIN=your-app.railway.app
```

## 🧪 Development

### Code Quality
- **Type Hints**: Full Python type annotations
- **ESLint**: JavaScript/React code quality
- **Documentation**: Comprehensive docstrings and READMEs
- **Error Handling**: Consistent error responses and logging

### Testing Strategy
- **Backend**: Unit tests for services, integration tests for APIs
- **Frontend**: Component testing, API integration testing
- **Database**: Migration testing and data validation

### Contributing
1. Follow existing code structure and patterns
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Ensure responsive design for frontend changes
5. Test across different devices and browsers

## 📊 System Architecture

### Data Flow
1. **Document Upload** → PDF/DOCX processing
2. **AI Analysis** → Case extraction and suggestions
3. **Case Creation** → Database storage with followups
4. **Task Assignment** → User assignment and tracking
5. **Progress Monitoring** → Status updates and completion

### Security Features
- **JWT Authentication**: Secure token-based auth
- **Role-based Access**: Admin and user permissions
- **Data Anonymization**: GDPR-compliant data handling
- **Input Validation**: Comprehensive request validation
- **CORS Protection**: Production-ready CORS configuration

## 🔍 Monitoring & Logging

### Backend Logging
- Structured logging with configurable levels
- Request/response logging middleware
- Error tracking and exception handling
- Health check endpoints

### Frontend Monitoring
- Error boundaries for React components
- API error handling and user feedback
- Performance monitoring and optimization
- Responsive design validation

## 🚨 Troubleshooting

### Common Issues

#### Backend
- **Database Connection**: Check DATABASE_URL and credentials
- **AI Processing**: Verify OPENAI_API_KEY is valid
- **Port Conflicts**: Ensure port 8000 is available

#### Frontend
- **API Connection**: Verify backend is running and accessible
- **Build Errors**: Check Node.js version and dependencies
- **CORS Issues**: Ensure backend CORS settings match frontend URL

### Debug Mode
Set `ENVIRONMENT=development` to enable:
- Interactive API documentation
- Detailed error messages
- Development-specific CORS settings
- Hot reload for development

## 📈 Performance & Scalability

### Backend Optimization
- **Async Processing**: FastAPI async/await for concurrent requests
- **Database Optimization**: Efficient queries and indexing
- **Caching**: Response caching for frequently accessed data
- **Load Balancing**: Ready for horizontal scaling

### Frontend Optimization
- **Code Splitting**: Route-based code splitting
- **Lazy Loading**: Component lazy loading
- **Bundle Optimization**: Tree shaking and minification
- **CDN Ready**: Static asset optimization

## 🤝 Support & Community

### Documentation
- **Backend**: See `backend/README.md` for detailed API docs
- **Frontend**: See `frontend/README.md` for component docs
- **API**: Interactive docs at `/docs` endpoint

### Getting Help
1. Check the troubleshooting section above
2. Review the detailed README files in each directory
3. Examine the API documentation at `/docs`
4. Check the code comments and docstrings

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**Built with ❤️ for modern guest relations management**
