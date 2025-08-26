# Railway Deployment Guide

This guide will help you deploy the Guest Relations Management System to Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Push your code to GitHub
3. **OpenAI API Key**: Get your API key from [OpenAI](https://platform.openai.com)

## Step 1: Prepare Your Repository

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Verify Files**: Ensure these files are in your repository:
   - `railway.json`
   - `nixpacks.toml`
   - `Procfile`
   - `railway.env.example`

## Step 2: Create Railway Project

1. **Login to Railway**: Go to [railway.app](https://railway.app) and sign in
2. **New Project**: Click "New Project"
3. **Deploy from GitHub**: Select "Deploy from GitHub repo"
4. **Select Repository**: Choose your Guest Relations repository
5. **Deploy**: Railway will automatically detect the configuration and start building

## Step 3: Add Database Service

1. **Add MySQL**: In your Railway project dashboard, click "New Service"
2. **Database**: Select "Database" → "MySQL"
3. **Wait for Setup**: Railway will provision a MySQL database
4. **Get Connection String**: Copy the `DATABASE_URL` from the database service

## Step 4: Configure Environment Variables

1. **Go to Variables**: In your main service, click on "Variables" tab
2. **Add Variables**: Add the following environment variables:

```env
# Database (Railway provides this automatically)
DATABASE_URL=mysql+pymysql://username:password@host:port/database

# JWT Configuration
SECRET_KEY=your-super-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Environment
ENVIRONMENT=production
LOG_LEVEL=INFO

# CORS (Railway will provide the domain automatically)
ALLOWED_ORIGINS=https://your-app-name.railway.app
```

## Step 5: Deploy and Setup Database

1. **Deploy**: Railway will automatically deploy your application
2. **Check Logs**: Monitor the deployment logs for any issues
3. **Run Migrations**: Once deployed, run database migrations:

```bash
# Connect to your Railway service
railway connect

# Run migrations
railway run alembic upgrade head

# Seed initial data
railway run python seed_users.py
```

## Step 6: Access Your Application

1. **Get URL**: Railway will provide a public URL (e.g., `https://your-app-name.railway.app`)
2. **Test Health**: Visit `https://your-app-name.railway.app/health`
3. **Access App**: Visit `https://your-app-name.railway.app` to access the frontend

## Railway CLI (Optional)

Install Railway CLI for easier management:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Deploy
railway up

# View logs
railway logs

# Connect to database
railway connect
```

## Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://user:pass@host:port/db` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `ENVIRONMENT` | Environment type | `production` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | `30` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ALLOWED_ORIGINS` | CORS origins | Auto-detected |

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check the build logs in Railway dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify Node.js and Python versions

2. **Database Connection Issues**:
   - Verify `DATABASE_URL` is correct
   - Check if MySQL service is running
   - Run migrations manually

3. **CORS Issues**:
   - Update `ALLOWED_ORIGINS` with your Railway domain
   - Check browser console for CORS errors

4. **Static Files Not Loading**:
   - Verify frontend build completed successfully
   - Check if `static` directory exists in backend

### Debug Commands

```bash
# View logs
railway logs

# Connect to service
railway shell

# Run commands
railway run python manage.py migrate
railway run python seed_users.py

# Check environment
railway run env
```

## Custom Domain (Optional)

1. **Add Custom Domain**: In Railway dashboard, go to "Settings" → "Domains"
2. **Add Domain**: Enter your custom domain
3. **Update DNS**: Point your domain to Railway's provided CNAME
4. **Update CORS**: Update `ALLOWED_ORIGINS` with your custom domain

## Monitoring and Maintenance

### Health Checks

Railway automatically monitors your application:
- Health check endpoint: `/health`
- Automatic restarts on failure
- Resource monitoring

### Logs

Access logs through:
- Railway dashboard
- Railway CLI: `railway logs`
- Real-time monitoring

### Updates

To update your application:
1. Push changes to GitHub
2. Railway automatically redeploys
3. Monitor logs for any issues

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to Git
2. **SECRET_KEY**: Use a strong, random secret key
3. **Database**: Railway provides secure database connections
4. **HTTPS**: Railway automatically provides HTTPS
5. **CORS**: Restrict origins to your domains only

## Cost Optimization

1. **Resource Limits**: Set appropriate resource limits
2. **Auto-sleep**: Enable auto-sleep for development
3. **Database**: Use appropriate database size
4. **Monitoring**: Monitor usage in Railway dashboard

## Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Community**: [Railway Discord](https://discord.gg/railway)
- **GitHub Issues**: Create issues in your repository

## Quick Commands

```bash
# Deploy
railway up

# View logs
railway logs

# Connect to database
railway connect

# Run migrations
railway run alembic upgrade head

# Seed data
railway run python seed_users.py

# Check status
railway status
```
