# Docker Troubleshooting Guide

## Common Issues and Solutions

### 1. Frontend Build Failures

**Error**: `npm run build` fails with exit code 127
**Solution**: 
- Ensure Node.js version compatibility
- Check if all dependencies are properly installed
- Verify package.json scripts

**Fix**:
```bash
# Clean and rebuild
docker-compose down
docker system prune -f
docker-compose build --no-cache
```

### 2. Backend Build Failures

**Error**: `apt-get update` fails or times out
**Solution**:
- Check internet connectivity
- Try using different base image
- Increase build timeout

**Fix**:
```bash
# Use different base image or add retry logic
FROM python:3.11-slim
RUN apt-get update --fix-missing
```

### 3. Database Connection Issues

**Error**: Backend can't connect to database
**Solution**:
- Ensure database container is healthy
- Check database credentials
- Verify network connectivity

**Fix**:
```bash
# Check database status
docker-compose ps
docker-compose logs db

# Test database connection
docker-compose exec backend python -c "from db import engine; print(engine.execute('SELECT 1').fetchone())"
```

### 4. Memory Issues

**Error**: Build process killed (exit code 137)
**Solution**:
- Increase Docker memory allocation
- Optimize build process
- Use multi-stage builds

**Fix**:
```bash
# Increase Docker memory in Docker Desktop settings
# Or use build with less memory:
docker-compose build --parallel
```

### 5. Port Conflicts

**Error**: Port already in use
**Solution**:
- Stop conflicting services
- Change port mappings
- Use different ports

**Fix**:
```bash
# Stop all containers
docker-compose down

# Check what's using the port
netstat -tulpn | grep :8000

# Kill the process or change port in docker-compose.yml
```

### 6. Permission Issues

**Error**: Permission denied when accessing files
**Solution**:
- Check file permissions
- Ensure proper user setup
- Fix volume mounts

**Fix**:
```bash
# Fix permissions
sudo chown -R $USER:$USER .
chmod -R 755 .

# Or run with proper user in Dockerfile
USER app
```

## Debugging Commands

### Check Container Status
```bash
docker-compose ps
docker-compose logs [service_name]
```

### Inspect Container
```bash
docker-compose exec [service_name] /bin/bash
docker inspect [container_id]
```

### Check Resource Usage
```bash
docker stats
docker system df
```

### Clean Up
```bash
# Remove all containers and volumes
docker-compose down -v

# Remove all unused resources
docker system prune -a

# Remove specific images
docker rmi [image_id]
```

## Build Optimization

### 1. Use .dockerignore
Create `.dockerignore` file:
```
node_modules
.git
*.log
.env
.DS_Store
```

### 2. Multi-stage Builds
```dockerfile
# Build stage
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

### 3. Layer Caching
```dockerfile
# Copy package files first (changes less frequently)
COPY package*.json ./
RUN npm ci

# Copy source code last (changes more frequently)
COPY . .
```

## Environment-Specific Issues

### Development
```bash
# Use development compose file
docker-compose -f docker-compose.dev.yml up

# Enable hot reload
docker-compose up --build
```

### Production
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f
```

## Performance Tips

### 1. Build Time Optimization
- Use specific base image versions
- Minimize layers
- Use multi-stage builds
- Cache dependencies

### 2. Runtime Optimization
- Use health checks
- Set resource limits
- Use proper restart policies
- Monitor resource usage

### 3. Network Optimization
- Use internal networks
- Minimize exposed ports
- Use reverse proxy
- Enable compression

## Common Docker Compose Issues

### 1. Service Dependencies
```yaml
services:
  backend:
    depends_on:
      db:
        condition: service_healthy
```

### 2. Environment Variables
```yaml
services:
  backend:
    environment:
      - DATABASE_URL=mysql://user:pass@db:3306/db
    env_file:
      - .env
```

### 3. Volume Mounts
```yaml
services:
  backend:
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
```

## Getting Help

### 1. Check Logs
```bash
docker-compose logs [service_name]
docker logs [container_id]
```

### 2. Debug Mode
```bash
docker-compose up --build --force-recreate
```

### 3. Interactive Debugging
```bash
docker-compose exec [service_name] /bin/bash
```

### 4. Health Checks
```bash
curl http://localhost:8000/health
docker-compose ps
```

## Quick Fixes

### Reset Everything
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Rebuild Specific Service
```bash
docker-compose build [service_name]
docker-compose up [service_name]
```

### Check Resource Usage
```bash
docker stats
docker system df
```

### View All Containers
```bash
docker ps -a
docker images
```
