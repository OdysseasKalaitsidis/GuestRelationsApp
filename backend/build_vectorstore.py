#!/usr/bin/env python3
"""
Script to build vectorstore from documents in the data folder.
This should be run by administrators to update the AI training data.
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

def build_vectorstore(data_folder="data", persist_folder="vectorstore"):
    """
    Build vectorstore from documents in the data folder.
    
    Args:
        data_folder: Path to folder containing training documents
        persist_folder: Path where vectorstore will be saved
    """
    
    if not os.path.exists(data_folder):
        logger.error(f"Data folder '{data_folder}' does not exist!")
        return False
    
    documents = []
    
    # Process all files in the data folder
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        
        if os.path.isfile(file_path):
            try:
                logger.info(f"Processing file: {filename}")
                
                if filename.endswith(".txt"):
                    loader = TextLoader(file_path, encoding="utf-8")
                    documents.extend(loader.load())
                    
                elif filename.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                    
                elif filename.endswith(".md"):
                    loader = TextLoader(file_path, encoding="utf-8")
                    documents.extend(loader.load())
                    
                else:
                    logger.warning(f"Skipping unsupported file type: {filename}")
                    
            except Exception as e:
                logger.error(f"Error processing {filename}: {str(e)}")
                continue
    
    if not documents:
        logger.warning("No documents found to process!")
        return False
    
    logger.info(f"Found {len(documents)} documents to process")
    
    # Split documents into chunks
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_documents(documents)
    
    logger.info(f"Split into {len(texts)} chunks")
    
    # Create embeddings and vectorstore
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)
    
    # Save vectorstore
    vectorstore.save_local(persist_folder)
    logger.info(f"✅ Vector store saved to: {persist_folder}/")
    
    return True

def main():
    """Main function to run the vectorstore build process."""
    
    print("🤖 Building AI Training Vectorstore")
    print("=" * 50)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY not found in environment variables!")
        logger.error("Please set your OpenAI API key in the .env file")
        return False
    
    # Build vectorstore
    success = build_vectorstore()
    
    if success:
        print("\n✅ Vectorstore build completed successfully!")
        print("The AI assistant now has access to the training documents.")
    else:
        print("\n❌ Vectorstore build failed!")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
