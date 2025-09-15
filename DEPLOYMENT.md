# Deployment Guide

This guide covers deploying the Guest Relations AI App to production environments.

## 🚀 Quick Deployment Overview

- **Backend**: Deploy to Render, Railway, or similar Python hosting
- **Frontend**: Deploy to Netlify, Vercel, or similar static hosting
- **Database**: Use Supabase PostgreSQL
- **AI**: OpenAI API integration

## 📋 Prerequisites

Before deploying, ensure you have:

1. **Supabase Account**: For PostgreSQL database
2. **OpenAI API Key**: For AI features
3. **GitHub Repository**: With your code
4. **Deployment Platform Accounts**: Render/Netlify accounts

## 🗄️ Database Setup (Supabase)

### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and anon key

### 2. Database Configuration
```sql
-- The database schema will be created automatically via Alembic migrations
-- No manual setup required
```

### 3. Environment Variables
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
```

## 🔧 Backend Deployment (Render)

### 1. Connect Repository
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Select the repository

### 2. Create Web Service
1. Choose "Web Service"
2. Configure:
   - **Name**: `guest-relations-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

### 3. Environment Variables
Set these in Render dashboard:

```env
# Required
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_jwt_secret_key_here
ENVIRONMENT=production

# Optional
ALLOWED_ORIGINS=https://your-frontend-domain.com
LOG_LEVEL=INFO
```

### 4. Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Note the service URL (e.g., `https://your-app.onrender.com`)

## 🎨 Frontend Deployment (Netlify)

### 1. Connect Repository
1. Go to [netlify.com](https://netlify.com)
2. Connect your GitHub repository
3. Select the repository

### 2. Build Settings
Configure:
- **Build Command**: `npm run build`
- **Publish Directory**: `dist`
- **Base Directory**: `frontend`

### 3. Environment Variables
Set these in Netlify dashboard:

```env
# Required
VITE_API_URL=https://your-backend-url.onrender.com/api
VITE_ENVIRONMENT=production

# Optional
VITE_APP_NAME=Guest Relations AI App
VITE_APP_VERSION=1.0.0
```

### 4. Deploy
1. Click "Deploy site"
2. Wait for deployment to complete
3. Note the site URL (e.g., `https://your-site.netlify.app`)

## 🔄 Alternative Deployment Options

### Backend Alternatives

#### Railway
1. Connect GitHub repository
2. Set environment variables
3. Deploy with Python runtime

#### Heroku
1. Create Heroku app
2. Connect GitHub repository
3. Set environment variables
4. Deploy

#### DigitalOcean App Platform
1. Create app from GitHub
2. Configure Python service
3. Set environment variables
4. Deploy

### Frontend Alternatives

#### Vercel
1. Connect GitHub repository
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Deploy

#### GitHub Pages
1. Enable GitHub Pages in repository settings
2. Use GitHub Actions for deployment
3. Configure build workflow

## 🔐 Security Configuration

### 1. CORS Configuration
Update backend CORS origins:
```python
origins = [
    "https://your-frontend-domain.com",
    "https://your-frontend-domain.netlify.app",
    # Add other allowed origins
]
```

### 2. Environment Security
- Never commit `.env` files
- Use strong, random `SECRET_KEY`
- Rotate API keys regularly
- Enable HTTPS only

### 3. Database Security
- Use Supabase Row Level Security (RLS)
- Implement proper authentication
- Regular backups

## 📊 Monitoring and Logging

### 1. Backend Logging
```python
# Logging is configured in logging_config.py
# Logs are written to logs/app.log
```

### 2. Error Monitoring
Consider integrating:
- Sentry for error tracking
- LogRocket for frontend monitoring
- Uptime monitoring services

### 3. Performance Monitoring
- Monitor API response times
- Track database query performance
- Monitor frontend bundle size

## 🔄 CI/CD Pipeline

### GitHub Actions Example
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        # Add Render deployment step

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Netlify
        # Add Netlify deployment step
```

## 🧪 Testing Deployment

### 1. Health Checks
Test these endpoints after deployment:

```bash
# Backend health check
curl https://your-backend-url.onrender.com/api/ping

# Frontend accessibility
curl https://your-frontend-url.netlify.app
```

### 2. Functionality Tests
1. Test user registration/login
2. Test document upload
3. Test case creation
4. Test AI chat functionality

### 3. Performance Tests
- Test API response times
- Test file upload limits
- Test concurrent users

## 🚨 Troubleshooting

### Common Issues

#### Backend Issues
- **CORS errors**: Check allowed origins
- **Database connection**: Verify Supabase credentials
- **OpenAI errors**: Check API key and limits

#### Frontend Issues
- **API connection**: Verify backend URL
- **Build failures**: Check Node.js version
- **Environment variables**: Ensure proper prefix (VITE_)

#### Database Issues
- **Migration errors**: Run `alembic upgrade head`
- **Connection timeouts**: Check Supabase status
- **Permission errors**: Verify RLS policies

### Debug Commands
```bash
# Check backend logs
curl https://your-backend-url.onrender.com/api/debug/env

# Check CORS configuration
curl https://your-backend-url.onrender.com/api/debug/cors

# Test database connection
curl https://your-backend-url.onrender.com/api/debug/users
```

## 📈 Scaling Considerations

### Backend Scaling
- Use connection pooling for database
- Implement caching (Redis)
- Use CDN for static assets
- Consider microservices architecture

### Frontend Scaling
- Implement code splitting
- Use CDN for assets
- Optimize bundle size
- Implement lazy loading

### Database Scaling
- Use Supabase connection pooling
- Implement read replicas
- Optimize queries
- Consider database sharding

## 🔄 Updates and Maintenance

### 1. Regular Updates
- Update dependencies monthly
- Security patches immediately
- Monitor for breaking changes

### 2. Backup Strategy
- Automated database backups
- Code repository backups
- Environment configuration backups

### 3. Monitoring
- Set up uptime monitoring
- Monitor error rates
- Track performance metrics
- Set up alerts

## 📞 Support

If you encounter deployment issues:

1. Check the logs in your deployment platform
2. Verify environment variables
3. Test locally first
4. Check platform status pages
5. Review this documentation

For additional help, create an issue in the GitHub repository.

---

**Happy Deploying! 🚀**
