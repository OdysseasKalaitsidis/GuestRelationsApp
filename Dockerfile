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
FROM python:3.11-alpine

WORKDIR /app

# Install system dependencies for Alpine
RUN apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-dev \
    pkgconfig \
    curl

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .

# Install dependencies in very small batches to avoid memory issues
RUN pip install --no-cache-dir fastapi==0.104.1
RUN pip install --no-cache-dir uvicorn[standard]==0.24.0
RUN pip install --no-cache-dir sqlalchemy==2.0.23
RUN pip install --no-cache-dir pymysql==1.1.0
RUN pip install --no-cache-dir python-multipart==0.0.6
RUN pip install --no-cache-dir python-dotenv==1.0.0
RUN pip install --no-cache-dir openai==1.3.7
RUN pip install --no-cache-dir alembic==1.12.1
RUN pip install --no-cache-dir requests==2.31.0
RUN pip install --no-cache-dir python-jose[cryptography]==3.3.0
RUN pip install --no-cache-dir passlib[bcrypt]==1.7.4
RUN pip install --no-cache-dir email-validator==2.1.0
RUN pip install --no-cache-dir reportlab==4.0.7
RUN pip install --no-cache-dir PyPDF2==3.0.1
RUN pip install --no-cache-dir scikit-learn==1.3.2
RUN pip install --no-cache-dir numpy==1.24.3

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
