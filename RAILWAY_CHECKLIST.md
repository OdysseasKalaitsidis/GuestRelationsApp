# Railway Deployment Checklist

## Pre-Deployment

### Repository Setup
- [ ] Code pushed to GitHub
- [ ] All Railway configuration files present:
  - [ ] `railway.json`
  - [ ] `nixpacks.toml`
  - [ ] `Procfile`
  - [ ] `railway.env.example`

### Environment Variables
- [ ] `SECRET_KEY` - Strong, random secret key
- [ ] `OPENAI_API_KEY` - Valid OpenAI API key
- [ ] `ENVIRONMENT=production`
- [ ] `LOG_LEVEL=INFO`

## Deployment Steps

### 1. Create Railway Project
- [ ] Sign up/login to Railway
- [ ] Create new project
- [ ] Connect GitHub repository
- [ ] Select repository branch

### 2. Add Database
- [ ] Add MySQL database service
- [ ] Wait for database provisioning
- [ ] Copy `DATABASE_URL` from database service

### 3. Configure Environment
- [ ] Set `SECRET_KEY` in main service
- [ ] Set `OPENAI_API_KEY` in main service
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `LOG_LEVEL=INFO`
- [ ] Verify `DATABASE_URL` is automatically set

### 4. Deploy
- [ ] Trigger deployment
- [ ] Monitor build logs
- [ ] Wait for successful deployment
- [ ] Note the Railway URL

## Post-Deployment

### Database Setup
- [ ] Install Railway CLI: `npm install -g @railway/cli`
- [ ] Login: `railway login`
- [ ] Link project: `railway link`
- [ ] Run migrations: `railway run alembic upgrade head`
- [ ] Seed users: `railway run python seed_users.py`

### Testing
- [ ] Health check: `https://your-app.railway.app/health`
- [ ] Frontend access: `https://your-app.railway.app`
- [ ] API access: `https://your-app.railway.app/api`
- [ ] Login with default credentials:
  - Username: `admin`
  - Password: `admin123`

### Security
- [ ] Change default admin password
- [ ] Verify HTTPS is working
- [ ] Test CORS configuration
- [ ] Check environment variables are secure

## Verification

### Application Features
- [ ] User authentication works
- [ ] Case management functions
- [ ] Email AI assistant responds
- [ ] Task management works
- [ ] PDF upload/processing works
- [ ] Follow-up system functions

### Performance
- [ ] Application loads quickly
- [ ] API responses are fast
- [ ] Database queries are optimized
- [ ] Static files load properly

### Monitoring
- [ ] Health checks are working
- [ ] Logs are accessible
- [ ] Error tracking is enabled
- [ ] Resource usage is monitored

## Troubleshooting

### Common Issues
- [ ] Build failures - Check build logs
- [ ] Database connection - Verify DATABASE_URL
- [ ] CORS errors - Update ALLOWED_ORIGINS
- [ ] Static files - Check frontend build
- [ ] Environment variables - Verify all are set

### Debug Commands
```bash
# View logs
railway logs

# Check environment
railway run env

# Test database connection
railway run python -c "from db import engine; print('DB OK')"

# Run migrations manually
railway run alembic upgrade head

# Seed data manually
railway run python seed_users.py
```

## Maintenance

### Regular Tasks
- [ ] Monitor application logs
- [ ] Check resource usage
- [ ] Update dependencies
- [ ] Backup database
- [ ] Review security settings

### Updates
- [ ] Push code changes to GitHub
- [ ] Monitor Railway deployment
- [ ] Test after updates
- [ ] Update documentation

## Quick Commands

```bash
# Deploy
railway up

# View logs
railway logs

# Connect to service
railway shell

# Run migrations
railway run alembic upgrade head

# Seed data
railway run python seed_users.py

# Check status
railway status
```

## Support Resources

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues**: Create issues in your repository
- **Application Logs**: Check Railway dashboard

---

## Success Criteria

✅ **Deployment Complete When**:
- Application is accessible via Railway URL
- Health check returns 200 OK
- Database migrations completed
- Default user can login
- All major features work
- No critical errors in logs

🎉 **Your Guest Relations System is now live on Railway!**
