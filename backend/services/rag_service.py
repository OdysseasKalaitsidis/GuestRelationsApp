# backend/services/rag_service.py

import os
import json
import uuid
from typing import List, Dict, Any, Optional
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class RAGService:
    def __init__(self):
        """Initialize the RAG service with FAISS vector database and OpenAI client"""
        self.openai_client = self._get_openai_client()
        self.embeddings = OpenAIEmbeddings()
        
        # Initialize FAISS vector store
        self.persist_folder = "vectorstore"
        self.vectorstore = None
        self.environment = os.getenv("ENVIRONMENT", "development")
        self._load_or_create_vectorstore()
    
    def _get_openai_client(self) -> OpenAI:
        """Get OpenAI client"""
        api_key = Config.OPENAI_API_KEY
        if not api_key:
            raise RuntimeError("Missing OPENAI_API_KEY. Check your .env file.")
        return OpenAI(api_key=api_key)
    
    def _load_or_create_vectorstore(self):
        """Load existing vectorstore or create a new one from data folder"""
        try:
            if os.path.exists(self.persist_folder):
                self.vectorstore = FAISS.load_local(
                    self.persist_folder, 
                    self.embeddings, 
                    allow_dangerous_deserialization=True
                )
                logger.info(f"Loaded existing vectorstore from {self.persist_folder}")
            else:
                # Try to build vectorstore from data folder
                logger.info("No existing vectorstore found, attempting to build from data folder")
                self._build_from_data_folder()
        except Exception as e:
            logger.error(f"Error loading vectorstore: {str(e)}")
            self.vectorstore = None
    
    def _build_from_data_folder(self):
        """Build vectorstore from documents in the data folder"""
        data_folder = "data"
        
        if not os.path.exists(data_folder):
            logger.info("No data folder found, vectorstore will be empty")
            self.vectorstore = None
            return
        
        documents = []
        
        # Process all files in the data folder
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)
            
            if os.path.isfile(file_path):
                try:
                    logger.info(f"Processing file: {filename}")
                    
                    if filename.endswith(".txt") or filename.endswith(".md"):
                        loader = TextLoader(file_path, encoding="utf-8")
                        documents.extend(loader.load())
                        
                    elif filename.endswith(".pdf"):
                        loader = PyPDFLoader(file_path)
                        documents.extend(loader.load())
                        
                except Exception as e:
                    logger.error(f"Error processing {filename}: {str(e)}")
                    continue
        
        if not documents:
            logger.info("No documents found in data folder")
            self.vectorstore = None
            return
        
        logger.info(f"Found {len(documents)} documents to process")
        
        # Split documents into chunks
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = splitter.split_documents(documents)
        
        logger.info(f"Split into {len(texts)} chunks")
        
        # Create vectorstore
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)
        
        # Save vectorstore
        self.vectorstore.save_local(self.persist_folder)
        logger.info(f"✅ Vectorstore built and saved to: {self.persist_folder}/")
    
    def upload_training_documents(self, files: List[Any]) -> Dict[str, Any]:
        """
        Upload and process training documents for RAG system
        
        Args:
            files: List of uploaded files (documents, PDFs, etc.)
            
        Returns:
            Dict with upload results
        """
        results = {
            "uploaded_files": [],
            "processed_chunks": 0,
            "errors": []
        }
        
        documents = []
        
        for file in files:
            try:
                # Read file content
                content = file.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
                
                # Extract text based on file type
                text_content = self._extract_text_from_file(file.filename, content)
                
                if text_content:
                    # Create document object
                    doc = Document(
                        page_content=text_content,
                        metadata={"filename": file.filename}
                    )
                    documents.append(doc)
                    
                    results["uploaded_files"].append({
                        "filename": file.filename,
                        "status": "success"
                    })
                    
                    logger.info(f"Successfully processed {file.filename}")
                
            except Exception as e:
                error_msg = f"Error processing {file.filename}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
                results["uploaded_files"].append({
                    "filename": file.filename,
                    "status": "error",
                    "error": str(e)
                })
        
        # Process all documents together
        if documents:
            try:
                # Split documents into chunks
                splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                texts = splitter.split_documents(documents)
                
                # Create or update vectorstore
                if self.vectorstore is None:
                    self.vectorstore = FAISS.from_documents(texts, self.embeddings)
                else:
                    # Add new documents to existing vectorstore
                    new_vectorstore = FAISS.from_documents(texts, self.embeddings)
                    self.vectorstore.merge_from(new_vectorstore)
                
                # Save vectorstore
                self.vectorstore.save_local(self.persist_folder)
                
                results["processed_chunks"] = len(texts)
                logger.info(f"Successfully processed {len(texts)} chunks and saved vectorstore")
                
            except Exception as e:
                error_msg = f"Error creating vectorstore: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
        
        return results
    
    def _extract_text_from_file(self, filename: str, content: str) -> str:
        """Extract text content from various file types"""
        file_ext = Path(filename).suffix.lower()
        
        if file_ext == '.txt':
            return content
        elif file_ext == '.md':
            return content
        elif file_ext == '.pdf':
            # For PDF files, you might want to use PyPDF2 or pdfplumber
            # For now, assuming content is already extracted
            return content
        elif file_ext in ['.doc', '.docx']:
            # For Word documents, assuming content is already extracted
            return content
        else:
            # Default to treating as plain text
            return content
    
    def _split_text_into_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks for better retrieval"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                search_start = max(start + chunk_size - 100, start)
                for i in range(end, search_start, -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def process_email_with_rag(self, input_text: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Process input email text using RAG to generate a standardized email response
        
        Args:
            input_text: The input email text to process
            context: Optional additional context
            
        Returns:
            Dict with the generated email and metadata
        """
        try:
            if self.vectorstore is None:
                return {
                    "success": False,
                    "error": "No vectorstore available. Please upload training documents first.",
                    "input_text": input_text
                }
            
            # Retrieve relevant chunks from vector database
            docs = self.vectorstore.similarity_search(input_text, k=3)
            
            # Prepare context for OpenAI
            context_text = "\n".join([doc.page_content for doc in docs])
            
            # Generate email using OpenAI with RAG context
            system_prompt = """You are an expert email assistant that helps format and improve emails based on provided standards and templates.

Your task is to:
1. Analyze the input email text
2. Use the provided context (standards, templates, examples) to improve the email
3. Return a well-formatted, professional email that follows the standards
4. Maintain the original intent and key information
5. Improve tone, structure, and clarity as needed

Return the email in the following JSON format:
{
    "subject": "Email subject line",
    "body": "Formatted email body",
    "improvements": ["List of improvements made"],
    "tone": "Professional/Formal/Friendly/etc",
    "confidence": 0.95
}"""

            user_prompt = f"""Input email text to process:
{input_text}

{context if context else ""}

Relevant standards and templates:
{context_text}

Please process this email and return a formatted response following the standards provided."""

            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Parse the response
            result_text = response.choices[0].message.content.strip()
            
            # Clean up JSON response
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
            if result_text.startswith('json'):
                result_text = result_text[4:]
            
            result_text = result_text.strip()
            
            try:
                email_result = json.loads(result_text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                email_result = {
                    "subject": "Processed Email",
                    "body": result_text,
                    "improvements": ["Email processed using AI"],
                    "tone": "Professional",
                    "confidence": 0.7
                }
            
            return {
                "success": True,
                "email": email_result,
                "context_used": [{"content": doc.page_content, "source": doc.metadata.get("filename", "unknown")} for doc in docs],
                "input_text": input_text,
                "processing_info": {
                    "model": "gpt-4o-mini",
                    "chunks_retrieved": len(docs),
                    "total_chunks_available": len(self.vectorstore.docstore._dict) if self.vectorstore else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing email with RAG: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "input_text": input_text
            }
    
    def get_openai_reply(self, messages: List[Dict[str, str]]) -> str:
        """
        Get OpenAI reply with vector search context (similar to your previous project)
        """
        if self.vectorstore is None:
            return "I don't have access to training documents yet. Please upload some documents first."
        
        user_question = messages[-1]["content"]
        docs = self.vectorstore.similarity_search(user_question, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        system_prompt = {
            "role": "system",
            "content": (
                "You are a helpful assistant for the front desk at Domes of Corfu. "
                "Answer based on hotel policies, tone, and procedures. "
                "You are helping the personnel of the Front Desk and the Guest Relations Team; "
                "your answers are tailored to the personnel. "
                "Use the following context when relevant:\n\n" + context
            )
        }

        chat_log = [system_prompt] + messages

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=chat_log,
            temperature=0, 
            max_tokens=500
        )

        return response.choices[0].message.content

    def extract_shift_summary(self, notes: str) -> Dict[str, Any]:
        """
        Takes raw shift notes and returns a JSON with date, room moves, and highlights.
        """
        prompt = (
            "You are a hotel shift assistant. "
            "Here are the shift notes:\n"
            f"{notes}\n\n"
            "Please extract and return the following JSON object with these fields:\n"
            " - date: date of the shift (YYYY-MM-DD) if mentioned, else null\n"
            " - highlights: list of strings summarizing incidents\n\n"
            "Example output:\n"
            "{\n"
            '  "date": "2025-08-11",\n'
            '  "highlights": ["Late checkout requested in room 204", "Noise complaint in room 512 resolved"]\n'
            "}\n\n"
            "Return only the JSON, nothing else."
        )

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You summarize hotel shifts into structured JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=300,
        )

        text = response.choices[0].message.content

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {"error": "Failed to parse JSON from model output", "raw_output": text}

        return data

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the document collection"""
        try:
            if self.vectorstore is None:
                return {
                    "total_chunks": 0,
                    "status": "no_vectorstore",
                    "message": "No vectorstore available"
                }
            
            count = len(self.vectorstore.docstore._dict)
            return {
                "total_chunks": count,
                "status": "active",
                "persist_folder": self.persist_folder
            }
        except Exception as e:
            return {
                "total_chunks": 0,
                "status": "error",
                "error": str(e)
            }
    
    def clear_collection(self) -> Dict[str, Any]:
        """Clear all documents from the collection"""
        try:
            # Remove the vectorstore directory
            import shutil
            if os.path.exists(self.persist_folder):
                shutil.rmtree(self.persist_folder)
            
            # Reset vectorstore
            self.vectorstore = None
            
            return {"success": True, "message": "Collection cleared successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def rebuild_from_data_folder(self) -> Dict[str, Any]:
        """Rebuild vectorstore from documents in the data folder"""
        try:
            # Clear existing vectorstore
            if os.path.exists(self.persist_folder):
                import shutil
                shutil.rmtree(self.persist_folder)
            
            # Build new vectorstore from data folder
            self._build_from_data_folder()
            
            if self.vectorstore is not None:
                count = len(self.vectorstore.docstore._dict)
                return {
                    "success": True, 
                    "message": f"Vectorstore rebuilt successfully with {count} chunks",
                    "chunks": count
                }
            else:
                return {
                    "success": False, 
                    "message": "No documents found in data folder to rebuild vectorstore"
                }
                
        except Exception as e:
            logger.error(f"Error rebuilding vectorstore: {str(e)}")
            return {"success": False, "error": str(e)}

# Global instance
rag_service = RAGService()
