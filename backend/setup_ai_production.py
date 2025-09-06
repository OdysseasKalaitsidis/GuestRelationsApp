#!/usr/bin/env python3
"""
Simple production setup script for AI assistant.
This script builds the vectorstore from documents in the data folder.
"""

import os
import sys
from pathlib import Path
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_vectorstore_from_data_folder():
    """Build vectorstore from documents in the data folder"""
    
    data_folder = "data"
    persist_folder = "vectorstore"
    
    if not os.path.exists(data_folder):
        logger.error(f"❌ Data folder '{data_folder}' does not exist!")
        logger.error("Please create the data folder and add your training documents.")
        return False
    
    documents = []
    
    # Process all files in the data folder
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        
        if os.path.isfile(file_path):
            try:
                logger.info(f"📄 Processing file: {filename}")
                
                if filename.endswith(".txt") or filename.endswith(".md"):
                    loader = TextLoader(file_path, encoding="utf-8")
                    docs = loader.load()
                    # Add metadata
                    for doc in docs:
                        doc.metadata['source'] = filename
                    documents.extend(docs)
                    
                elif filename.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                    # Add metadata
                    for doc in docs:
                        doc.metadata['source'] = filename
                    documents.extend(docs)
                    
                else:
                    logger.warning(f"⚠️ Skipping unsupported file type: {filename}")
                    
            except Exception as e:
                logger.error(f"❌ Error processing {filename}: {str(e)}")
                continue
    
    if not documents:
        logger.warning("⚠️ No documents found to process!")
        return False
    
    logger.info(f"📚 Found {len(documents)} documents to process")
    
    # Split documents into chunks
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_documents(documents)
    
    logger.info(f"✂️ Split into {len(texts)} chunks")
    
    # Create embeddings and vectorstore
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)
    
    # Save vectorstore
    vectorstore.save_local(persist_folder)
    logger.info(f"✅ Vectorstore saved to: {persist_folder}/")
    
    return True

def main():
    """Main function to run the vectorstore build process."""
    
    print("🤖 Building AI Training Vectorstore for Production")
    print("=" * 60)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("❌ OPENAI_API_KEY not found in environment variables!")
        logger.error("Please set your OpenAI API key in the .env file")
        return False
    
    # Build vectorstore
    success = build_vectorstore_from_data_folder()
    
    if success:
        print("\n✅ Vectorstore build completed successfully!")
        print("🎯 The AI assistant is now ready for production!")
        print("\n📋 Next steps:")
        print("1. Deploy your application")
        print("2. The AI assistant will automatically load the vectorstore on startup")
        print("3. Users can now chat with the AI assistant")
    else:
        print("\n❌ Vectorstore build failed!")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you have documents in the 'data' folder")
        print("2. Check that your OpenAI API key is set correctly")
        print("3. Ensure all dependencies are installed")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
