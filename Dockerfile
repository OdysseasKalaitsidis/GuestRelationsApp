# Frontend build stage
FROM node:18-alpine AS frontend-build

# Install necessary build tools for Alpine
RUN apk add --no-cache python3 make g++

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies (including devDependencies for build)
RUN npm ci --prefer-offline --no-audit

# Copy source code
COPY frontend/ ./

# Set environment variables for build
ENV NODE_ENV=production
ENV GENERATE_SOURCEMAP=false

# Build the application
RUN npm run build

# Backend stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .

# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies with memory optimization and pre-compiled wheels
RUN pip install --no-cache-dir --only-binary=all -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/dist ./static

# Create necessary directories
RUN mkdir -p uploads logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
