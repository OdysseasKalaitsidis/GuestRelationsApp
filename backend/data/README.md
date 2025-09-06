# Training Documents Folder

This folder contains the training documents for the AI assistant. Only administrators should add documents to this folder.

## How to Add Training Documents

1. **Add Documents**: Place your training documents (PDF, TXT, MD files) in this `data` folder
2. **Build Vectorstore**: Run the build script to update the AI's knowledge base:

```bash
cd backend
python build_vectorstore.py
```

## Supported File Types

- **PDF files** (.pdf) - Hotel policies, procedures, manuals
- **Text files** (.txt) - Email templates, guidelines, notes
- **Markdown files** (.md) - Documentation, procedures

## Document Guidelines

For best results, ensure your documents contain:
- Hotel policies and procedures
- Email templates and examples
- Guest relations guidelines
- Standard operating procedures
- Common scenarios and responses

## Security Note

⚠️ **Important**: This folder is not accessible through the web interface. Only administrators with server access can add documents here. This ensures that only authorized personnel can update the AI's training data.

## After Adding Documents

After adding new documents to this folder, you must run the build script to update the AI's knowledge base:

```bash
python build_vectorstore.py
```

The AI assistant will then have access to the new information and can provide more accurate responses based on the updated training data.
