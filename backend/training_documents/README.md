# Training Documents Folder

This folder contains the training documents used by the Email AI Assistant for RAG (Retrieval-Augmented Generation).

## How to Use

1. **Add Training Files**: Place your PDF or TXT files in this folder
2. **Supported Formats**: 
   - PDF files (.pdf)
   - Text files (.txt)
3. **Content**: Add hotel policies, procedures, knowledge base content, or any relevant information that should be used to generate email responses

## Example Files

- `hotel_policies.txt` - Contains hotel policies and procedures
- `amenities_guide.pdf` - Information about hotel amenities
- `emergency_procedures.txt` - Emergency and safety procedures

## File Naming

Use descriptive names for your files:
- `check_in_policies.txt`
- `room_service_menu.pdf`
- `guest_complaint_procedures.txt`

## Notes

- The AI will automatically load all files from this folder when generating responses
- Files are processed using TF-IDF similarity search to find relevant content
- Only PDF and TXT files are supported
- Files are loaded automatically when the server starts
