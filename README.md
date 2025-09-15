# Guest Relations AI App

A modern, AI-powered guest relations management system built with FastAPI backend and React frontend. This application streamlines guest relations workflows with intelligent document processing, case management, and automated follow-ups.

## 🌟 Features

### 🤖 AI-Powered Document Processing
- **Smart PDF/DOCX Parsing**: Automatically extract guest information from documents
- **Intelligent Case Creation**: AI suggests case details and categorizes issues
- **RAG-Powered Assistant**: Chat with AI for policy questions and guidance

### 📋 Comprehensive Case Management
- **Full CRUD Operations**: Create, read, update, and delete guest relations cases
- **Status Tracking**: Monitor case progress from creation to resolution
- **Manual Input**: Add cases manually with intuitive forms
- **Template System**: Quick case creation with predefined templates

### 🔄 Automated Workflows
- **Document Upload Pipeline**: Seamless PDF processing workflow
- **Follow-up Management**: Track and manage guest follow-ups
- **Real-time Updates**: Live data synchronization across the application

### 🔐 Enterprise Security
- **JWT Authentication**: Secure user authentication and authorization
- **Role-based Access**: Admin and user permission levels
- **Data Anonymization**: Built-in privacy protection features
- **CORS Protection**: Secure cross-origin resource sharing

## 🏗️ Architecture

```
Guest Relations AI App/
├── backend/                    # FastAPI backend API
│   ├── main.py                # Application entry point
│   ├── models.py               # Database models
│   ├── routers/                # API route handlers
│   ├── services/               # Business logic layer
│   ├── schemas/                # Pydantic data models
│   ├── alembic/                # Database migrations
│   └── requirements.txt        # Python dependencies
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # Page components
│   │   └── services/           # API service layer
│   ├── package.json            # Node.js dependencies
│   └── vite.config.js          # Build configuration
└── README.md                   # This file
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: Supabase PostgreSQL with SQLAlchemy 2.0+
- **AI Integration**: OpenAI GPT for document analysis and chat
- **Authentication**: JWT with bcrypt password hashing
- **Document Processing**: PyPDF2, python-docx, spaCy
- **Deployment**: Render-ready with environment configuration

### Frontend
- **Framework**: React 18 with modern Hooks
- **Build Tool**: Vite for fast development and optimized builds
- **Styling**: Tailwind CSS for responsive design
- **Routing**: React Router for seamless navigation
- **HTTP Client**: Fetch API with centralized service layer
- **Deployment**: Netlify/Vercel ready

## 📋 Prerequisites

- **Python 3.11+** for backend development
- **Node.js 16+** for frontend development
- **Supabase Account** for PostgreSQL database
- **OpenAI API Key** for AI features
- **Git** for version control

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/guest-relations-ai-app.git
cd guest-relations-ai-app
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp env.example .env

# Edit .env with your configuration
# Required variables:
# - SUPABASE_URL=your_supabase_url
# - SUPABASE_KEY=your_supabase_anon_key
# - OPENAI_API_KEY=your_openai_api_key
# - SECRET_KEY=your_jwt_secret_key

# Run database migrations
alembic upgrade head

# Start development server
python main.py
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp env.example .env

# Edit .env with your API URL
# VITE_API_URL=http://localhost:8000/api

# Start development server
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Environment Configuration

### Backend Environment Variables (.env)
```env
# Database Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
DATABASE_URL=your_supabase_database_url

# AI Configuration
OPENAI_API_KEY=your_openai_api_key

# Security
SECRET_KEY=your_jwt_secret_key_here

# Environment
ENVIRONMENT=development

# Optional: Additional CORS origins
ALLOWED_ORIGINS=https://yourdomain.com,https://anotherdomain.com
```

### Frontend Environment Variables (.env)
```env
# API Configuration
VITE_API_URL=http://localhost:8000/api

# For production, use your deployed backend URL:
# VITE_API_URL=https://your-backend-url.com/api
```

## 📊 API Documentation

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user info

### Case Management
- `GET /api/cases` - List all cases
- `POST /api/cases` - Create new case
- `GET /api/cases/{id}` - Get case details
- `PUT /api/cases/{id}` - Update case
- `DELETE /api/cases/{id}` - Delete case
- `GET /api/cases/with-followups` - Get cases with follow-ups

### Document Processing
- `POST /api/documents/upload` - Upload document for processing
- `POST /api/documents/workflow` - Complete document workflow
- `GET /api/documents/{id}` - Get document details

### Follow-up Management
- `GET /api/followups` - List all follow-ups
- `POST /api/followups` - Create follow-up
- `PUT /api/followups/{id}` - Update follow-up
- `DELETE /api/followups/{id}` - Delete follow-up

### AI Assistant
- `POST /api/rag/chat` - Chat with AI assistant
- `GET /api/rag/stats` - Get RAG collection statistics

## 🚀 Deployment

### Backend Deployment (Render)
1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy with Python 3.11 runtime
4. Configure custom domain if needed

### Frontend Deployment (Netlify)
1. Connect your GitHub repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Configure environment variables
5. Deploy and configure custom domain

### Environment Variables for Production
Ensure these are set in your deployment platform:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `OPENAI_API_KEY`
- `SECRET_KEY`
- `ENVIRONMENT=production`

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📝 Development Guidelines

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ESLint configuration
- **Commits**: Use conventional commit messages
- **Documentation**: Update README for significant changes

### API Design
- Follow RESTful conventions
- Use proper HTTP status codes
- Implement comprehensive error handling
- Document all endpoints with OpenAPI

### Security Best Practices
- Never commit sensitive data
- Use environment variables for configuration
- Implement proper input validation
- Follow OWASP security guidelines

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Contribution Guidelines
- Write clear, descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Follow the existing code style
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. **Check the documentation** in the `/docs` folder
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Contact the maintainers** for urgent matters

## 🙏 Acknowledgments

- **FastAPI** for the excellent Python web framework
- **React** for the powerful frontend library
- **Supabase** for the backend-as-a-service platform
- **OpenAI** for AI capabilities
- **Tailwind CSS** for the utility-first CSS framework

---

**Made with ❤️ for modern guest relations management**
