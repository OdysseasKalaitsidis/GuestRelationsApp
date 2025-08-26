# Guest Relations System - Railway Deployment

## Quick Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/deploy)

## Manual Deployment Steps

1. **Fork this repository** to your GitHub account
2. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your forked repository

3. **Add MySQL Database**:
   - In Railway dashboard, click "New Service"
   - Select "Database" → "MySQL"

4. **Set Environment Variables**:
   ```env
   SECRET_KEY=your-super-secret-key-here
   OPENAI_API_KEY=your-openai-api-key
   ENVIRONMENT=production
   ```

5. **Deploy**: Railway will automatically build and deploy your application

## Features

- ✅ **Case Management**: Create and track guest relations cases
- ✅ **AI Email Assistant**: Generate professional email responses using RAG
- ✅ **Task Management**: Assign and track daily tasks
- ✅ **PDF Processing**: Upload and analyze PDF documents
- ✅ **User Authentication**: Secure login system
- ✅ **Real-time Updates**: Live status updates

## Access Your Application

Once deployed, you'll get a Railway URL like:
`https://your-app-name.railway.app`

- **Frontend**: `https://your-app-name.railway.app`
- **API**: `https://your-app-name.railway.app/api`
- **Health Check**: `https://your-app-name.railway.app/health`

## Default Login

After deployment, you can login with:
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change the default password after first login!

## Configuration

### Required Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | JWT secret key | ✅ |
| `OPENAI_API_KEY` | OpenAI API key for AI features | ✅ |
| `DATABASE_URL` | MySQL connection string | ✅ (Auto-provided) |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment type | `production` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | `30` |

## Database Setup

After deployment, run these commands to set up the database:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and connect
railway login
railway link

# Run migrations
railway run alembic upgrade head

# Seed initial data
railway run python seed_users.py
```

## Troubleshooting

### Common Issues

1. **Build Fails**: Check Railway build logs
2. **Database Connection**: Verify `DATABASE_URL` is set
3. **CORS Errors**: Update `ALLOWED_ORIGINS` with your Railway domain
4. **Static Files**: Ensure frontend build completed successfully

### Getting Help

- Check Railway build logs
- Verify environment variables
- Test health endpoint: `/health`
- Review application logs

## Custom Domain

To use a custom domain:

1. Add domain in Railway dashboard
2. Update DNS records
3. Update `ALLOWED_ORIGINS` environment variable

## Security

- Change default admin password
- Use strong `SECRET_KEY`
- Keep `OPENAI_API_KEY` secure
- Regularly update dependencies

## Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Issues**: Create GitHub issues
- **Community**: Railway Discord

---

**Ready to deploy?** Click the Railway button above or follow the manual steps!
