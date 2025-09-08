#!/usr/bin/env python3
"""
RAG Retraining Script
Automatically retrains the RAG system by rebuilding the vectorstore from all documents in the data folder.
"""

import os
import sys
import logging
import requests
import json
from pathlib import Path
from typing import List, Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RAGRetrainer:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        """
        Initialize the RAG retrainer
        
        Args:
            base_url: Base URL of the API server
            api_key: API key for authentication (optional for local development)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get current collection statistics"""
        try:
            response = requests.get(
                f"{self.base_url}/api/rag/stats",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {"error": str(e)}
    
    def clear_collection(self) -> Dict[str, Any]:
        """Clear the existing RAG collection"""
        try:
            logger.info("Clearing existing RAG collection...")
            response = requests.delete(
                f"{self.base_url}/api/rag/clear-collection",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"Collection cleared: {result.get('message', 'Success')}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to clear collection: {e}")
            return {"error": str(e)}
    
    def rebuild_from_data_folder(self) -> Dict[str, Any]:
        """Rebuild vectorstore from data folder"""
        try:
            logger.info("Rebuilding vectorstore from data folder...")
            response = requests.post(
                f"{self.base_url}/api/rag/rebuild-from-data",
                headers=self.headers,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"Vectorstore rebuilt: {result.get('message', 'Success')}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to rebuild vectorstore: {e}")
            return {"error": str(e)}
    
    def upload_training_documents(self, data_folder: str = "data") -> Dict[str, Any]:
        """Upload all documents from the data folder"""
        data_path = Path(data_folder)
        if not data_path.exists():
            logger.error(f"Data folder '{data_folder}' does not exist")
            return {"error": f"Data folder '{data_folder}' does not exist"}
        
        # Find all supported document files
        supported_extensions = {'.txt', '.md', '.pdf', '.doc', '.docx'}
        files = []
        
        for file_path in data_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                files.append(file_path)
        
        if not files:
            logger.error(f"No supported documents found in '{data_folder}'")
            return {"error": f"No supported documents found in '{data_folder}'"}
        
        logger.info(f"Found {len(files)} documents to upload:")
        for file_path in files:
            logger.info(f"  - {file_path.name}")
        
        try:
            # Prepare files for upload
            files_data = []
            for file_path in files:
                with open(file_path, 'rb') as f:
                    files_data.append(('files', (file_path.name, f.read(), 'application/octet-stream')))
            
            # Upload files
            logger.info("Uploading training documents...")
            response = requests.post(
                f"{self.base_url}/api/rag/upload-documents",
                files=files_data,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Upload completed:")
            logger.info(f"  - Files uploaded: {len(result.get('uploaded_files', []))}")
            logger.info(f"  - Chunks processed: {result.get('processed_chunks', 0)}")
            logger.info(f"  - Errors: {len(result.get('errors', []))}")
            
            if result.get('errors'):
                for error in result['errors']:
                    logger.warning(f"  - Error: {error}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to upload documents: {e}")
            return {"error": str(e)}
    
    def test_rag_system(self) -> Dict[str, Any]:
        """Test the RAG system to verify it's working"""
        try:
            logger.info("Testing RAG system...")
            response = requests.post(
                f"{self.base_url}/api/rag/test-rag",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('success'):
                logger.info("✅ RAG system test passed")
            else:
                logger.error(f"❌ RAG system test failed: {result.get('error', 'Unknown error')}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to test RAG system: {e}")
            return {"error": str(e)}
    
    def retrain(self, method: str = "rebuild", data_folder: str = "data") -> bool:
        """
        Retrain the RAG system using the specified method
        
        Args:
            method: "rebuild" (from data folder) or "upload" (clear and re-upload)
            data_folder: Path to the data folder containing training documents
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("🚀 Starting RAG retraining process...")
        
        # Get initial stats
        logger.info("📊 Getting initial collection stats...")
        initial_stats = self.get_collection_stats()
        if "error" not in initial_stats:
            logger.info(f"  - Initial chunks: {initial_stats.get('total_chunks', 0)}")
        
        success = False
        
        if method == "rebuild":
            # Method 1: Rebuild from data folder
            logger.info("🔄 Using rebuild method...")
            result = self.rebuild_from_data_folder()
            success = "error" not in result
            
        elif method == "upload":
            # Method 2: Clear and re-upload
            logger.info("🔄 Using clear and re-upload method...")
            
            # Clear collection
            clear_result = self.clear_collection()
            if "error" in clear_result:
                logger.error("Failed to clear collection")
                return False
            
            # Upload documents
            upload_result = self.upload_training_documents(data_folder)
            success = "error" not in upload_result
            
        else:
            logger.error(f"Unknown method: {method}. Use 'rebuild' or 'upload'")
            return False
        
        if success:
            # Get final stats
            logger.info("📊 Getting final collection stats...")
            final_stats = self.get_collection_stats()
            if "error" not in final_stats:
                logger.info(f"  - Final chunks: {final_stats.get('total_chunks', 0)}")
            
            # Test the system
            test_result = self.test_rag_system()
            if test_result.get('success'):
                logger.info("✅ RAG retraining completed successfully!")
                return True
            else:
                logger.error("❌ RAG retraining completed but system test failed")
                return False
        else:
            logger.error("❌ RAG retraining failed")
            return False

def main():
    """Main function to run the retraining script"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Retrain the RAG system")
    parser.add_argument(
        "--method", 
        choices=["rebuild", "upload"], 
        default="rebuild",
        help="Retraining method: 'rebuild' (from data folder) or 'upload' (clear and re-upload)"
    )
    parser.add_argument(
        "--data-folder", 
        default="data",
        help="Path to the data folder containing training documents"
    )
    parser.add_argument(
        "--base-url", 
        default="http://localhost:8000",
        help="Base URL of the API server"
    )
    parser.add_argument(
        "--api-key", 
        help="API key for authentication (optional for local development)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize retrainer
    retrainer = RAGRetrainer(
        base_url=args.base_url,
        api_key=args.api_key
    )
    
    # Run retraining
    success = retrainer.retrain(
        method=args.method,
        data_folder=args.data_folder
    )
    
    if success:
        logger.info("🎉 RAG retraining completed successfully!")
        sys.exit(0)
    else:
        logger.error("💥 RAG retraining failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
