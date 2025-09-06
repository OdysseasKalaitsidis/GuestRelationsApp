# Guest Relations Management System

A production-ready system for managing guest relations cases with AI-powered document processing and workflow automation. Built with FastAPI backend and React frontend.

## 🏗️ Architecture

```
GR_Domes/
├── backend/                    # FastAPI backend API
│   ├── main.py                # Application entry point
│   ├── models.py               # Database models
│   ├── db.py                   # Database connection
│   ├── requirements.txt        # Python dependencies
│   ├── routers/                # API route handlers
│   ├── services/               # Business logic layer
│   ├── schemas/                # Pydantic data models
│   └── alembic/                # Database migrations
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # Page components
│   │   └── services/           # API service layer
│   ├── package.json            # Node.js dependencies
│   └── vite.config.js          # Build configuration
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
- **Database**: SQLAlchemy 2.0+ with Supabase PostgreSQL
- **AI**: OpenAI integration for document analysis
- **Authentication**: JWT with bcrypt
- **Document Processing**: PyPDF2, python-docx, spaCy
- **Deployment**: Render-ready with environment config

### Frontend
- **Framework**: React 18 with Hooks
- **Build Tool**: Vite for fast development
- **Styling**: Tailwind CSS utility framework
- **Routing**: React Router for navigation
- **HTTP**: Fetch API with centralized service layer

## 📋 Prerequisites

- **Python 3.11** for backend
- **Node.js 16+** for frontend
- **Supabase PostgreSQL** database
- **OpenAI API key** for AI features

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Create .env file with your configuration
cp .env.example .env
# Edit .env with your actual values

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
cp .env.example .env
# Edit .env with your API URL

# Run development server
npm run dev
```

## 🔧 Environment Configuration

### Backend (.env)
```env
DATABASE_URL=your_supabase_database_url
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_jwt_secret_key
ENVIRONMENT=development
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
```

## 📊 API Endpoints

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

## 🚀 Deployment

### Backend (Render)
1. Connect your GitHub repository
2. Set environment variables
3. Deploy with Python 3.11 runtime

### Frontend (Netlify/Vercel)
1. Connect your GitHub repository
2. Set build command: `npm run build`
3. Set publish directory: `dist`

## 📝 Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend components
- Implement proper error handling
- Write comprehensive API documentation
- Use environment variables for configuration
- Follow RESTful API conventions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
