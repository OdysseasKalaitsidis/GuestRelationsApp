# Production Deployment Guide

## Backend Configuration

### Environment Variables
Create a `.env` file in the backend directory with the following variables:

```env
# Database Configuration
DB_PASSWORD=your_secure_password_here

# JWT Configuration
SECRET_KEY=your_super_secret_jwt_key_here_change_this_in_production

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Production Settings
ENVIRONMENT=production
DEBUG=false
```

### Database Setup
1. Create a MySQL database named `mydb`
2. Create a user `myuser` with the password from your `.env` file
3. Grant all privileges on `mydb` to `myuser`

### Dependencies Installation
```bash
cd backend
pip install -r requirements.txt
```

### Database Migration
```bash
# Create tables
python create_tables.py

# Seed initial users
python seed_users.py
```

### Running the Backend
```bash
# Development
python run.py

# Production (with Gunicorn)
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

## Frontend Configuration

### Environment Variables
Create a `.env.local` file in the frontend directory:

```env
# API Configuration
VITE_API_URL=https://your-api-domain.com/api

# App Configuration
VITE_APP_NAME=Guest Relations System
VITE_APP_VERSION=1.0.0
```

### Dependencies Installation
```bash
cd frontend
npm install
```

### Building for Production
```bash
npm run build
```

### Serving the Frontend
```bash
# Development
npm run dev

# Production (serve the dist folder with nginx or similar)
```

## Security Considerations

1. **Change default passwords** - Update all default passwords in production
2. **Use HTTPS** - Always use HTTPS in production
3. **Environment variables** - Never commit `.env` files to version control
4. **Database security** - Use strong passwords and limit database access
5. **JWT secret** - Use a strong, random JWT secret key
6. **CORS configuration** - Update CORS origins for production domains

## Default User Accounts

The system comes with 5 default users:

### Admin Accounts
- Username: `admin1` / Password: `admin123`
- Username: `admin2` / Password: `admin123`

### Regular User Accounts
- Username: `john_smith` / Password: `user123`
- Username: `sarah_johnson` / Password: `user123`
- Username: `mike_davis` / Password: `user123`

**⚠️ IMPORTANT: Change these default passwords in production!**

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user info

### Users
- `GET /api/users/` - Get all users (authenticated)
- `GET /api/users/{id}` - Get user by ID
- `POST /api/users/` - Create user (admin only)
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user (admin only)

### Cases
- `GET /api/cases/` - Get all cases
- `GET /api/cases/with-followups` - Get cases with followups
- `GET /api/cases/{id}` - Get case by ID
- `POST /api/cases/` - Create case
- `POST /api/cases/bulk` - Create multiple cases

### Followups
- `GET /api/followups/` - Get all followups
- `GET /api/followups/{id}` - Get followup by ID
- `POST /api/followups/` - Create followup
- `PUT /api/followups/{id}` - Update followup
- `DELETE /api/followups/{id}` - Delete followup

### PDF & AI
- `POST /api/pdf/upload` - Upload and process PDF
- `POST /api/ai/feedback` - Generate AI feedback
- `POST /api/workflow/complete` - Complete workflow

## Monitoring & Logging

1. **Application logs** - Monitor application logs for errors
2. **Database logs** - Monitor database performance
3. **API monitoring** - Set up API monitoring and alerting
4. **User activity** - Monitor user login and activity patterns

## Backup Strategy

1. **Database backups** - Regular automated database backups
2. **File uploads** - Backup uploaded PDF files
3. **Configuration** - Backup environment configuration
4. **Code deployment** - Use version control and deployment pipelines
