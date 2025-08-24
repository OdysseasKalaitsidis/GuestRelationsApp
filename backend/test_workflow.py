#!/usr/bin/env python3
"""
Test the workflow endpoint
"""

import requests
import json

def test_workflow_endpoint():
    """Test the workflow endpoint"""
    url = "http://localhost:8000/workflow/complete"
    
    # Create a simple test PDF file (just text content)
    test_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test PDF Content) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000200 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n292\n%%EOF"
    
    # Test the endpoint
    try:
        files = {'file': ('test.pdf', test_content, 'application/pdf')}
        response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Workflow endpoint working!")
        else:
            print("❌ Workflow endpoint failed")
            
    except Exception as e:
        print(f"❌ Error testing workflow: {e}")

if __name__ == "__main__":
    test_workflow_endpoint() 