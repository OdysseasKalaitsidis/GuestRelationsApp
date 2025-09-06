# RAG Email Processing System

This system provides a Retrieval-Augmented Generation (RAG) solution for processing emails using OpenAI's API and a vector database to store and retrieve email standards and templates.

## Features

- **Document Upload**: Upload training documents (standards, templates, examples)
- **Vector Storage**: Documents are processed and stored in ChromaDB for efficient retrieval
- **Email Processing**: Input email text is processed using RAG to generate standardized responses
- **No Database Storage**: Only training documents are stored; no user data is persisted

## API Endpoints

### Upload Training Documents
```
POST /api/rag/upload-documents
```
Upload documents that will be used as training data for the RAG system.

**Parameters:**
- `files`: List of files (supports .txt, .md, .pdf, .doc, .docx)

**Response:**
```json
{
  "uploaded_files": [
    {
      "filename": "email_standards.md",
      "chunks": 15,
      "status": "success"
    }
  ],
  "processed_chunks": 15,
  "errors": []
}
```

### Process Email
```
POST /api/rag/process-email
```
Process an email using the RAG system to generate a standardized response.

**Request Body:**
```json
{
  "input_text": "Hello, I have a complaint about my recent stay...",
  "context": "Optional additional context"
}
```

**Response:**
```json
{
  "success": true,
  "email": {
    "subject": "Re: Your Recent Stay - Complaint Resolution",
    "body": "Dear [Guest Name],\n\nThank you for taking the time to share your feedback...",
    "improvements": ["Added professional greeting", "Structured complaint response"],
    "tone": "Professional",
    "confidence": 0.95
  },
  "context_used": [
    {
      "content": "Complaint response template...",
      "source": "email_standards.md",
      "relevance_score": 0.92
    }
  ],
  "input_text": "Hello, I have a complaint about my recent stay...",
  "processing_info": {
    "model": "gpt-4o-mini",
    "chunks_retrieved": 3,
    "total_chunks_available": 15
  }
}
```

### Get Collection Statistics
```
GET /api/rag/stats
```
Get information about the document collection.

**Response:**
```json
{
  "total_chunks": 15,
  "collection_name": "email_standards",
  "status": "active"
}
```

### Clear Collection
```
DELETE /api/rag/clear-collection
```
Remove all training documents from the vector database.

**Response:**
```json
{
  "success": true,
  "message": "Collection cleared successfully"
}
```

### Test RAG System
```
POST /api/rag/test-rag
```
Test endpoint to verify the RAG system is working correctly.

## Setup Instructions

1. **Install Dependencies**: The required packages are already added to `requirements.txt`:
   - `chromadb==0.4.15`
   - `sentence-transformers==2.2.2`
   - `langchain==0.0.350`
   - `langchain-openai==0.0.2`
   - `faiss-cpu==1.7.4`

2. **Environment Variables**: Ensure you have `OPENAI_API_KEY` set in your `.env` file.

3. **Upload Training Documents**: Use the `/api/rag/upload-documents` endpoint to upload your email standards and templates.

4. **Process Emails**: Use the `/api/rag/process-email` endpoint to process incoming emails.

## Usage Example

1. **Upload Training Data**:
   ```bash
   curl -X POST "http://localhost:8000/api/rag/upload-documents" \
        -H "Content-Type: multipart/form-data" \
        -F "files=@email_standards.md"
   ```

2. **Process an Email**:
   ```bash
   curl -X POST "http://localhost:8000/api/rag/process-email" \
        -H "Content-Type: application/json" \
        -d '{
          "input_text": "Hi, I need help with my reservation for next week. Can you please check if room 205 is available?"
        }'
   ```

## File Structure

- `backend/services/rag_service.py`: Core RAG service implementation
- `backend/routers/rag_router.py`: FastAPI router with endpoints
- `backend/email_standards_template.md`: Example training document

## Technical Details

- **Vector Database**: ChromaDB for storing document embeddings
- **Embedding Model**: `all-MiniLM-L6-v2` for generating embeddings
- **LLM**: OpenAI GPT-4o-mini for text generation
- **Storage**: Local file system (`./rag_data` directory)
- **Chunking**: Text is split into 1000-character chunks with 200-character overlap

## Security Notes

- No user data is stored in the database
- Only training documents are persisted
- All processing is done in-memory for each request
- Vector database is stored locally and not shared
