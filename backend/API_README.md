# Guest Relations API Documentation

## Overview
This API provides endpoints for managing guest relations cases, including PDF upload, AI feedback generation, case management, and followup tracking.

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. PDF Processing
#### Upload and Process PDF
```
POST /pdf/upload
```
**Description**: Upload a PDF file and extract structured case data
**Request**: Multipart form with PDF file
**Response**: List of extracted cases with structured data

### 2. AI Feedback
#### Generate AI Suggestions
```
POST /ai/feedback
```
**Description**: Generate AI-powered feedback suggestions for cases
**Request**: JSON with list of cases
**Response**: List of AI suggestions with confidence scores

### 3. Complete Workflow
#### End-to-End Processing
```
POST /workflow/complete
```
**Description**: Complete workflow: PDF → AI → Cases → Followups
**Request**: Multipart form with PDF file
**Response**: Complete workflow status with created cases and followups

### 4. Case Management
#### Create Single Case
```
POST /cases/
```
**Description**: Create a single case
**Request**: JSON with case data
**Response**: Created case

#### Create Multiple Cases
```
POST /cases/bulk
```
**Description**: Create multiple cases at once
**Request**: JSON array of cases
**Response**: Array of created cases

#### Get All Cases
```
GET /cases/
```
**Description**: Retrieve all cases
**Response**: Array of cases

#### Get Cases with Followups
```
GET /cases/with-followups
```
**Description**: Retrieve all cases with their associated followups
**Response**: Array of cases with nested followup data

#### Get Specific Case
```
GET /cases/{case_id}
```
**Description**: Retrieve a specific case by ID
**Response**: Single case

### 5. Followup Management
#### Create Followup
```
POST /followups/
```
**Description**: Create a new followup
**Request**: JSON with followup data
**Response**: Created followup

#### Get All Followups
```
GET /followups/
```
**Description**: Retrieve all followups
**Response**: Array of followups

#### Get Specific Followup
```
GET /followups/{followup_id}
```
**Description**: Retrieve a specific followup by ID
**Response**: Single followup

#### Update Followup
```
PUT /followups/{followup_id}
```
**Description**: Update an existing followup
**Request**: JSON with updated followup data
**Response**: Updated followup

#### Delete Followup
```
DELETE /followups/{followup_id}
```
**Description**: Delete a followup
**Response**: Success status

## Data Models

### Case
```json
{
  "id": 1,
  "room": "101",
  "status": "pending",
  "importance": "high",
  "type": "maintenance",
  "title": "Broken faucet",
  "action": "Plumber called",
  "owner_id": 1
}
```

### Followup
```json
{
  "id": 1,
  "case_id": 1,
  "suggestion_text": "Follow up with guest to confirm repair completion",
  "status": "pending",
  "assigned_to": 2
}
```

### AI Feedback Response
```json
{
  "case_id": 0,
  "suggestion_text": "Contact guest to schedule follow-up inspection",
  "confidence": 0.85,
  "case_data": {...}
}
```

## Workflow Steps

1. **PDF Upload**: Upload PDF file via `/pdf/upload`
2. **AI Processing**: Send extracted cases to `/ai/feedback` for suggestions
3. **Case Creation**: Create cases in database via `/cases/bulk`
4. **Followup Creation**: Create followups with AI suggestions
5. **Assignment**: Assign followups to team members
6. **Tracking**: Monitor followup status and completion

## Running the API

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_openai_api_key
   DB_PASSWORD=your_database_password
   ```

3. Run the server:
   ```bash
   python run.py
   ```

4. Access the API at `http://localhost:8000`

5. View interactive docs at `http://localhost:8000/docs` 