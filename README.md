# Guest Relations AI App

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.0+-61dafb.svg)](https://reactjs.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

[![React](https://img.shields.io/badge/React-18-blue?logo=react)](https://reactjs.org/) 
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue?logo=postgresql)](https://www.postgresql.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT-purple?logo=openai)](https://openai.com/)

**AI-powered guest relations system** showcasing full-stack development, AI document processing, and workflow automation.  
**For educational and portfolio purposes only.**



---

## 🚀 Key Features

- **AI Document Processing:** Auto-extract guest info from PDFs/DOCX  
- **Case Management:** CRUD, status tracking, follow-ups, templates  
- **Automated Workflows:** Document upload pipeline & live updates  
- **Security:** JWT auth, role-based access, data anonymization  
- **AI Assistant:** Chat with AI for policy guidance  

---

## 🛠 Tech Stack

- **Backend:** FastAPI, PostgreSQL (Supabase), OpenAI GPT, PyPDF2, python-docx  
- **Frontend:** React 18, Vite, Tailwind CSS, React Router  
- **Deployment:** Render (backend), Netlify/Vercel (frontend)  

---

## 💡 What You Can Learn / Demonstrates

- Full-stack development (FastAPI + React)  
- AI integration in real-world workflows  
- File parsing & structured data handling  
- Secure authentication & role-based access  
- Clean, modular project architecture  

---

## ⚠️ Legal Disclaimer

- **Personal project**; non-commercial.  
- **Not affiliated** with Domes Resorts, Domes Operator, or Domes of Corfu.  
- **No real hotel data** is used; all content is AI-generated.  
- Sensitive data has been **removed**.  
- This repo is **for code demonstration only**.  
## ⚡ Quick Start

```bash
# Clone the repo
git clone https://github.com/yourusername/guest-relations-ai-app.git

# Backend
cd backend
pip install -r requirements.txt
cp env.example .env
# configure .env
python main.py

# Frontend
cd frontend
npm install
cp env.example .env
# configure .env
npm run dev
