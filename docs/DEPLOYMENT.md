# Deployment Guide

This guide details how to deploy the Guest Relations AI App to production environments.

## Prerequisites

- **GitHub Account** (for repository hosting)
- **Render Account** (for Backend hosting)
- **Netlify/Vercel Account** (for Frontend hosting)
- **Supabase Project** (Database & Storage)
- **OpenAI API Key**

## 1. Database Setup (Supabase)

1. Create a new project in Supabase.
2. Go to **SQL Editor** and run the initial schema (found in `backend/alembic/versions` or root `schema.sql` if available).
3. Enable `pgvector` extension:
    ```sql
    create extension vector;
    ```
4. Get your connection strings from **Project Settings > Database**.

## 2. Backend Deployment (Render)

We recommend [Render](https://render.com) for hosting the FastAPI backend.

1. **New Web Service**: Connect your GitHub repository.
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
    Add the following variables in the dashboard:
    - `python_version`: `3.11.0`
    - `SUPABASE_URL`: `your_supabase_url`
    - `SUPABASE_KEY`: `your_supabase_anon_key`
    - `DATABASE_URL`: `your_postgres_connection_string`
    - `OPENAI_API_KEY`: `your_openai_key`
    - `SECRET_KEY`: `generated_strong_random_string`
    - `ENVIRONMENT`: `production`

## 3. Frontend Deployment (Netlify)

We recommend [Netlify](https://netlify.com) for hosting the React frontend.

1. **New Site from Git**: Connect your GitHub repository.
2. **Build Command**: `npm run build`
3. **Publish Directory**: `dist`
4. **Environment Variables**:
    - `VITE_API_URL`: The URL of your deployed Render backend (e.g., `https://your-app.onrender.com/api`)
    - `VITE_ENVIRONMENT`: `production`

## 4. Post-Deployment Verification

1. **Health Check**: Visit `https://your-backend.onrender.com/health` (if endpoint exists) or root `/docs`.
2. **Frontend Load**: Visit your Netlify URL and verify the login page loads.
3. **Login Test**: Attempt to log in to verify database connection and JWT signing.
4. **CORS Check**: If you get network errors, update `ALLOWED_ORIGINS` in Backend environment variables to include your Netlify URL.

## Troubleshooting

### CORS Errors
If the browser console shows CORS errors:
1. Go to Render Dashboard.
2. Update `ALLOWED_ORIGINS` variable.
3. Add your frontend URL (e.g., `https://my-app.netlify.app`).
4. Redeploy Backend.

### Database Connection Issues
- Ensure `DATABASE_URL` is correct.
- For Supabase transaction pooler (port 6543), ensure your SQLAlchemy driver supports prepared statements or uses session pooler (port 5432).

### Build Failures
- **Backend**: Check `requirements.txt` for conflicting versions.
- **Frontend**: Check `package.json` and ensure strictly typed errors are handled.
