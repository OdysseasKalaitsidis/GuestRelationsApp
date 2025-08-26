# Railway Deployment Guide

This guide will help you deploy your Guest Relations System to Railway.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. Your project code in a Git repository (GitHub, GitLab, or Bitbucket)
3. A MySQL database (Railway provides MySQL add-ons)

## Step 1: Connect Your Repository

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub repo" (or your preferred Git provider)
4. Choose your repository
5. Railway will automatically detect your project structure

## Step 2: Configure Environment Variables

1. In your Railway project dashboard, go to the "Variables" tab
2. Add the following environment variables based on `railway.env.example`:

### Required Variables:
```
DATABASE_URL=mysql://username:password@host:port/database_name
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
ENVIRONMENT=production
```

### Optional Variables:
```
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://your-frontend-domain.com
MAX_FILE_SIZE=10485760
LOG_LEVEL=INFO
```

## Step 3: Add MySQL Database

1. In your Railway project, click "New"
2. Select "Database" → "MySQL"
3. Railway will automatically create a MySQL database
4. Copy the `DATABASE_URL` from the database service
5. Add it to your environment variables

## Step 4: Deploy

1. Railway will automatically start building and deploying your application
2. The build process will:
   - Install Node.js dependencies for the frontend
   - Build the React frontend
   - Install Python dependencies for the backend
   - Start the FastAPI server

## Step 5: Configure Custom Domain (Optional)

1. Go to your service settings
2. Click "Domains"
3. Add your custom domain
4. Configure DNS records as instructed

## Step 6: Database Migration

After deployment, you may need to run database migrations:

1. Go to your Railway project dashboard
2. Click on your backend service
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Open the terminal and run:
```bash
cd backend
alembic upgrade head
```

## Monitoring and Logs

- **Logs**: View real-time logs in the Railway dashboard
- **Metrics**: Monitor CPU, memory, and network usage
- **Health Checks**: Railway automatically monitors your `/health` endpoint

## Troubleshooting

### Common Issues:

1. **Build Failures**: Check the build logs in Railway dashboard
2. **Database Connection**: Verify `DATABASE_URL` is correct
3. **Environment Variables**: Ensure all required variables are set
4. **Port Issues**: Railway automatically sets the `PORT` environment variable

### Useful Commands:

```bash
# Check application status
curl https://your-app.railway.app/health

# View logs
railway logs

# Connect to database
railway connect mysql
```

## File Structure

Railway will automatically detect and build your application based on:
- `railway.json` - Railway-specific configuration
- `nixpacks.toml` - Build configuration
- `Procfile` - Process definition
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node.js dependencies

## Security Notes

1. Never commit sensitive environment variables to your repository
2. Use Railway's environment variable system for secrets
3. Enable HTTPS in production
4. Regularly update dependencies

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Railway Status: [status.railway.app](https://status.railway.app)
