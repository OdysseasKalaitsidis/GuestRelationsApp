#!/usr/bin/env python3
"""
Production-ready script to manage AI training documents.
This script handles document storage in Supabase Storage for production environments.
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from typing import List, Dict, Any
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import logging
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionDocumentManager:
    """Manages documents in production using Supabase Storage"""
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not all([self.supabase_url, self.supabase_key, self.openai_api_key]):
            raise ValueError("Missing required environment variables: SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY")
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.embeddings = OpenAIEmbeddings()
        self.bucket_name = "ai-training-docs"
        self.vectorstore_folder = "vectorstore"
        
    def ensure_bucket_exists(self):
        """Ensure the storage bucket exists"""
        try:
            # Try to get bucket info
            response = self.supabase.storage.get_bucket(self.bucket_name)
            logger.info(f"✅ Bucket '{self.bucket_name}' exists")
        except Exception:
            # Create bucket if it doesn't exist
            try:
                self.supabase.storage.create_bucket(
                    self.bucket_name,
                    options={"public": False}
                )
                logger.info(f"✅ Created bucket '{self.bucket_name}'")
            except Exception as e:
                logger.error(f"❌ Failed to create bucket: {e}")
                raise
    
    def upload_document_to_storage(self, file_path: str, filename: str) -> bool:
        """Upload a document to Supabase Storage"""
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Upload to storage
            response = self.supabase.storage.from_(self.bucket_name).upload(
                path=filename,
                file=file_data,
                file_options={"content-type": "application/octet-stream"}
            )
            
            logger.info(f"✅ Uploaded {filename} to storage")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to upload {filename}: {e}")
            return False
    
    def download_documents_from_storage(self) -> List[Document]:
        """Download all documents from Supabase Storage and convert to Langchain Documents"""
        documents = []
        
        try:
            # List all files in the bucket
            files = self.supabase.storage.from_(self.bucket_name).list()
            
            if not files:
                logger.info("No documents found in storage")
                return documents
            
            # Create temporary directory for downloaded files
            with tempfile.TemporaryDirectory() as temp_dir:
                for file_info in files:
                    filename = file_info['name']
                    file_path = os.path.join(temp_dir, filename)
                    
                    try:
                        # Download file
                        file_data = self.supabase.storage.from_(self.bucket_name).download(filename)
                        
                        # Save to temporary file
                        with open(file_path, 'wb') as f:
                            f.write(file_data)
                        
                        # Load document based on file type
                        if filename.endswith('.txt') or filename.endswith('.md'):
                            loader = TextLoader(file_path, encoding='utf-8')
                            docs = loader.load()
                            # Add metadata about source
                            for doc in docs:
                                doc.metadata['source'] = filename
                                doc.metadata['storage_type'] = 'supabase'
                            documents.extend(docs)
                            
                        elif filename.endswith('.pdf'):
                            loader = PyPDFLoader(file_path)
                            docs = loader.load()
                            # Add metadata about source
                            for doc in docs:
                                doc.metadata['source'] = filename
                                doc.metadata['storage_type'] = 'supabase'
                            documents.extend(docs)
                        
                        logger.info(f"✅ Processed {filename}")
                        
                    except Exception as e:
                        logger.error(f"❌ Failed to process {filename}: {e}")
                        continue
            
        except Exception as e:
            logger.error(f"❌ Failed to download documents from storage: {e}")
        
        return documents
    
    def upload_vectorstore_to_storage(self, vectorstore_path: str):
        """Upload the built vectorstore to Supabase Storage"""
        try:
            # Create a zip file of the vectorstore
            import zipfile
            import shutil
            
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
                with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(vectorstore_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, vectorstore_path)
                            zipf.write(file_path, arcname)
                
                # Upload zip file
                with open(temp_zip.name, 'rb') as f:
                    zip_data = f.read()
                
                self.supabase.storage.from_(self.bucket_name).upload(
                    path="vectorstore.zip",
                    file=zip_data,
                    file_options={"content-type": "application/zip"}
                )
                
                logger.info("✅ Uploaded vectorstore to storage")
                
                # Clean up temp file
                os.unlink(temp_zip.name)
                
        except Exception as e:
            logger.error(f"❌ Failed to upload vectorstore: {e}")
            raise
    
    def download_vectorstore_from_storage(self, local_path: str) -> bool:
        """Download and extract vectorstore from Supabase Storage"""
        try:
            # Download vectorstore zip
            zip_data = self.supabase.storage.from_(self.bucket_name).download("vectorstore.zip")
            
            # Extract to local path
            import zipfile
            with tempfile.NamedTemporaryFile(suffix='.zip') as temp_zip:
                temp_zip.write(zip_data)
                temp_zip.flush()
                
                with zipfile.ZipFile(temp_zip.name, 'r') as zipf:
                    zipf.extractall(local_path)
            
            logger.info("✅ Downloaded and extracted vectorstore from storage")
            return True
            
        except Exception as e:
            logger.info(f"ℹ️ No vectorstore found in storage: {e}")
            return False
    
    def build_vectorstore_from_storage(self, persist_folder: str = "vectorstore") -> bool:
        """Build vectorstore from documents in Supabase Storage"""
        try:
            logger.info("🔄 Building vectorstore from Supabase Storage...")
            
            # Download documents from storage
            documents = self.download_documents_from_storage()
            
            if not documents:
                logger.warning("No documents found in storage")
                return False
            
            logger.info(f"📚 Found {len(documents)} documents to process")
            
            # Split documents into chunks
            splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = splitter.split_documents(documents)
            
            logger.info(f"✂️ Split into {len(texts)} chunks")
            
            # Create vectorstore
            vectorstore = FAISS.from_documents(texts, self.embeddings)
            
            # Save locally
            vectorstore.save_local(persist_folder)
            logger.info(f"💾 Saved vectorstore locally to: {persist_folder}/")
            
            # Upload to storage
            self.upload_vectorstore_to_storage(persist_folder)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to build vectorstore: {e}")
            return False
    
    def load_vectorstore_from_storage(self, persist_folder: str = "vectorstore") -> bool:
        """Load vectorstore from Supabase Storage"""
        try:
            # Try to download vectorstore from storage
            if self.download_vectorstore_from_storage(persist_folder):
                logger.info("✅ Loaded vectorstore from Supabase Storage")
                return True
            else:
                # If no vectorstore in storage, try to build from documents
                logger.info("🔄 No vectorstore in storage, building from documents...")
                return self.build_vectorstore_from_storage(persist_folder)
                
        except Exception as e:
            logger.error(f"❌ Failed to load vectorstore from storage: {e}")
            return False

def main():
    """Main function for production document management"""
    print("🏭 Production AI Training Document Manager")
    print("=" * 50)
    
    try:
        manager = ProductionDocumentManager()
        
        # Ensure storage bucket exists
        manager.ensure_bucket_exists()
        
        # Build vectorstore from storage
        success = manager.build_vectorstore_from_storage()
        
        if success:
            print("\n✅ Production vectorstore build completed successfully!")
            print("The AI assistant now has access to training documents from Supabase Storage.")
        else:
            print("\n❌ Production vectorstore build failed!")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Production setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
