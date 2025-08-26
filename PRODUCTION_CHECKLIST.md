# Production Deployment Checklist

## Pre-Deployment

### Environment Configuration
- [ ] Create `.env` file in backend directory with production values
- [ ] Set `ENVIRONMENT=production` in backend `.env`
- [ ] Configure `DATABASE_URL` with production database credentials
- [ ] Set strong `SECRET_KEY` for JWT tokens
- [ ] Add OpenAI API key
- [ ] Configure `ALLOWED_ORIGINS` with production domain(s)
- [ ] Set `LOG_LEVEL=INFO` or `WARNING` for production

### Database Setup
- [ ] Create production MySQL database
- [ ] Run database migrations: `alembic upgrade head`
- [ ] Seed initial users: `python seed_users.py`
- [ ] Verify database connections and permissions

### Security
- [ ] Update CORS origins to production domains only
- [ ] Configure trusted hosts in nginx.conf
- [ ] Set up SSL certificates
- [ ] Review and update JWT token expiration
- [ ] Ensure all API endpoints require authentication

### File Permissions
- [ ] Set proper permissions for uploads directory
- [ ] Ensure logs directory is writable
- [ ] Check file ownership for all application files

## Deployment

### Using Docker (Recommended)
- [ ] Run `./deploy.sh` script
- [ ] Verify all containers are running: `docker-compose ps`
- [ ] Check application health: `curl http://localhost/health`
- [ ] Test frontend access: `curl http://localhost`
- [ ] Verify API endpoints are accessible

### Manual Deployment
- [ ] Build frontend: `cd frontend && npm run build`
- [ ] Copy built files to web server directory
- [ ] Configure web server (nginx/apache) to serve static files
- [ ] Set up reverse proxy for API endpoints
- [ ] Start backend server with production settings

## Post-Deployment

### Testing
- [ ] Test user authentication and login
- [ ] Verify all major features work:
  - [ ] Case management
  - [ ] PDF upload and processing
  - [ ] Email AI assistant
  - [ ] Task management
  - [ ] Follow-up system
- [ ] Test file uploads and downloads
- [ ] Verify email functionality (if applicable)

### Monitoring
- [ ] Set up application monitoring
- [ ] Configure log aggregation
- [ ] Set up database monitoring
- [ ] Monitor disk space for uploads and logs
- [ ] Set up alerts for critical errors

### Backup
- [ ] Set up database backups
- [ ] Configure file backup for uploads
- [ ] Test backup restoration process
- [ ] Document backup procedures

## Performance Optimization

### Frontend
- [ ] Enable gzip compression in web server
- [ ] Set up CDN for static assets (optional)
- [ ] Configure browser caching headers
- [ ] Optimize images and assets

### Backend
- [ ] Configure database connection pooling
- [ ] Set up Redis for caching (optional)
- [ ] Optimize database queries
- [ ] Configure rate limiting

### Infrastructure
- [ ] Set up load balancing (if needed)
- [ ] Configure auto-scaling (if using cloud)
- [ ] Monitor resource usage
- [ ] Set up health checks

## Security Hardening

### Application
- [ ] Review and update all passwords
- [ ] Enable HTTPS only
- [ ] Set up security headers
- [ ] Regular security updates
- [ ] Review access logs

### Server
- [ ] Update operating system
- [ ] Configure firewall rules
- [ ] Set up intrusion detection
- [ ] Regular security scans

## Documentation

### User Documentation
- [ ] Update user manual
- [ ] Create admin guide
- [ ] Document API endpoints
- [ ] Create troubleshooting guide

### Technical Documentation
- [ ] Update deployment procedures
- [ ] Document configuration options
- [ ] Create maintenance procedures
- [ ] Update architecture documentation

## Maintenance

### Regular Tasks
- [ ] Monitor application logs
- [ ] Check disk space usage
- [ ] Review error rates
- [ ] Update dependencies
- [ ] Backup verification

### Updates
- [ ] Plan for regular updates
- [ ] Test updates in staging environment
- [ ] Document rollback procedures
- [ ] Schedule maintenance windows

## Emergency Procedures

### Incident Response
- [ ] Document incident response procedures
- [ ] Set up alerting system
- [ ] Create escalation procedures
- [ ] Test emergency contacts

### Recovery
- [ ] Document disaster recovery procedures
- [ ] Test backup restoration
- [ ] Create recovery time objectives
- [ ] Plan for data recovery

---

## Quick Commands

### Docker Deployment
```bash
./deploy.sh
```

### Check Status
```bash
docker-compose ps
docker-compose logs -f
```

### Stop Application
```bash
docker-compose down
```

### Update Application
```bash
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database Operations
```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Seed users
docker-compose exec backend python seed_users.py

# Access database
docker-compose exec db mysql -u myuser -p mydb
```
