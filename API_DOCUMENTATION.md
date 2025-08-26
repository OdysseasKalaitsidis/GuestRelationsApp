# Guest Relations API Documentation

## Base URL
- Development: `http://localhost:8000/api`
- Production: `https://yourdomain.com/api`

## Authentication

All API endpoints (except login) require authentication using JWT tokens.

### Login
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "name": "Administrator",
    "is_admin": true
  }
}
```

### Using the Token
Include the token in the Authorization header:
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Endpoints

### Authentication

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>
```

### Users

#### Get All Users
```http
GET /api/users/
Authorization: Bearer <token>
```

### Cases

#### Get All Cases
```http
GET /api/cases/
Authorization: Bearer <token>
```

#### Get Cases with Followups
```http
GET /api/cases/with-followups
Authorization: Bearer <token>
```

#### Create Case
```http
POST /api/cases/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Guest Complaint",
  "description": "Room service issue",
  "guest_name": "John Doe",
  "room_number": "101",
  "priority": "medium"
}
```

#### Update Case Status
```http
PUT /api/cases/{case_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "resolved"
}
```

### Followups

#### Get All Followups
```http
GET /api/followups/with-case-info
Authorization: Bearer <token>
```

#### Create Followup
```http
POST /api/followups/
Authorization: Bearer <token>
Content-Type: application/json

{
  "case_id": 1,
  "action": "Called guest to resolve issue",
  "assigned_to": 2,
  "due_date": "2024-01-15"
}
```

#### Update Followup
```http
PUT /api/followups/{followup_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "completed",
  "notes": "Issue resolved successfully"
}
```

#### Delete Followup
```http
DELETE /api/followups/{followup_id}
Authorization: Bearer <token>
```

### Tasks

#### Get All Tasks
```http
GET /api/tasks/
Authorization: Bearer <token>
```

#### Create Task
```http
POST /api/tasks/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Daily Amenity Check",
  "description": "Check all room amenities",
  "task_type": "amenity_list",
  "assigned_to": 1,
  "due_date": "2024-01-15"
}
```

#### Create Daily Tasks
```http
POST /api/tasks/daily?task_date=2024-01-15
Authorization: Bearer <token>
```

#### Update Task
```http
PUT /api/tasks/{task_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "completed"
}
```

#### Delete Task
```http
DELETE /api/tasks/{task_id}
Authorization: Bearer <token>
```

### PDF Processing

#### Upload PDF
```http
POST /api/pdf/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <pdf_file>
```

### AI Services

#### Generate AI Feedback
```http
POST /api/ai/feedback
Authorization: Bearer <token>
Content-Type: application/json

{
  "cases": [
    {
      "id": 1,
      "title": "Guest Complaint",
      "description": "Room service issue"
    }
  ]
}
```

### Chat/Email Assistant

#### Chat with Email Assistant
```http
POST /api/chat/email-assistant
Authorization: Bearer <token>
Content-Type: application/json

{
  "email_content": "Dear Hotel Manager, I had an issue with my room service order..."
}
```

**Response:**
```json
{
  "response": "Dear Valued Guest,\n\nThank you for bringing this matter to our attention...",
  "relevant_documents": 3
}
```

### Training Documents

#### Get Training Documents
```http
GET /api/training/documents
Authorization: Bearer <token>
```

### Workflow

#### Complete Workflow
```http
POST /api/workflow/complete
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <pdf_file>
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication expired. Please login again."
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Data Models

### User
```json
{
  "id": 1,
  "username": "admin",
  "name": "Administrator",
  "is_admin": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Case
```json
{
  "id": 1,
  "title": "Guest Complaint",
  "description": "Room service issue",
  "guest_name": "John Doe",
  "room_number": "101",
  "status": "open",
  "priority": "medium",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Followup
```json
{
  "id": 1,
  "case_id": 1,
  "action": "Called guest to resolve issue",
  "status": "pending",
  "assigned_to": 2,
  "due_date": "2024-01-15",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Task
```json
{
  "id": 1,
  "title": "Daily Amenity Check",
  "description": "Check all room amenities",
  "task_type": "amenity_list",
  "status": "pending",
  "assigned_to": 1,
  "due_date": "2024-01-15",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- 100 requests per minute per IP address
- 1000 requests per hour per authenticated user

## WebSocket Support

Real-time updates are available via WebSocket connections:
- Connection: `ws://localhost:8000/ws`
- Authentication: Include JWT token in connection headers
- Events: case_updates, task_updates, followup_updates

## SDK Examples

### JavaScript/React
```javascript
import { login, fetchCases, createCase } from './services/api';

// Login
const response = await login('username', 'password');
const token = response.access_token;

// Fetch cases
const cases = await fetchCases();

// Create case
const newCase = await createCase({
  title: 'New Case',
  description: 'Case description',
  guest_name: 'John Doe',
  room_number: '101'
});
```

### Python
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login', 
                        data={'username': 'admin', 'password': 'password'})
token = response.json()['access_token']

# Fetch cases
headers = {'Authorization': f'Bearer {token}'}
cases = requests.get('http://localhost:8000/api/cases/', headers=headers)
```

## Testing

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "environment": "production"
}
```

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
