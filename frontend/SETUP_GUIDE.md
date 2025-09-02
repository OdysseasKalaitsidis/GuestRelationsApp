# Frontend Setup Guide for Deployed Backend

## ✅ Backend Status
Your backend is successfully deployed and running at:
**https://guestrelationsapp.onrender.com**

## 🔧 Frontend Configuration

### 1. Environment Variables
Create a `.env.local` file in the frontend directory with:

```env
VITE_API_URL=https://guestrelationsapp.onrender.com/api
VITE_ENVIRONMENT=production
VITE_APP_NAME=Guest Relations
```

### 2. Current API Configuration
Your frontend is already configured to use the deployed backend:
- **Development**: Uses proxy to localhost:8000
- **Production**: Uses https://guestrelationsapp.onrender.com/api

### 3. Available API Endpoints

#### Health Check
```
GET https://guestrelationsapp.onrender.com/api/health
Response: {"status":"healthy","environment":"production","database":"available"}
```

#### Authentication
```
POST https://guestrelationsapp.onrender.com/api/auth/login
```

#### Document Processing
```
POST https://guestrelationsapp.onrender.com/api/documents/upload
POST https://guestrelationsapp.onrender.com/api/documents/workflow
```

#### Cases Management
```
GET https://guestrelationsapp.onrender.com/api/cases/
POST https://guestrelationsapp.onrender.com/api/cases/
```

#### Followups
```
GET https://guestrelationsapp.onrender.com/api/followups/
POST https://guestrelationsapp.onrender.com/api/followups/
```

## 🚀 Deployment Steps

### 1. Build Frontend
```bash
cd frontend
npm install
npm run build
```

### 2. Deploy to Netlify/Vercel
- Upload the `dist` folder
- Set environment variables in your hosting platform
- Configure custom domain if needed

### 3. Test Connection
Open browser console and run:
```javascript
fetch('https://guestrelationsapp.onrender.com/api/health')
  .then(res => res.json())
  .then(data => console.log('API Status:', data));
```

## 🔍 Testing

### API Health Check
```bash
curl https://guestrelationsapp.onrender.com/api/health
```

### Frontend-Backend Connection
1. Open your frontend in browser
2. Open Developer Tools (F12)
3. Go to Console tab
4. Run the test script from `test-api-connection.js`

## 📝 Notes

- ✅ Backend is live and working
- ✅ Supabase database is connected
- ✅ CORS is configured for your frontend domains
- ✅ All API endpoints are available
- ✅ Authentication system is ready

## 🎯 Next Steps

1. **Deploy Frontend**: Build and deploy to your hosting platform
2. **Test Authentication**: Try logging in with your credentials
3. **Test Document Upload**: Upload a PDF to test the workflow
4. **Monitor Logs**: Check Render logs for any issues

Your Guest Relations application is ready to use! 🎉
