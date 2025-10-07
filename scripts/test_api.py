#!/usr/bin/env python3
"""
API Testing Script for Academic Assignment Helper
This script tests the main API endpoints to ensure they're working correctly.
"""

import requests
import json
import time
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@student.com"
TEST_PASSWORD = "password123"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("Health check passed")
            return True
        else:
            print(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Health check error: {str(e)}")
        return False

def test_login():
    """Test student login"""
    print("Testing student login...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )
        if response.status_code == 200:
            data = response.json()
            print("Login successful")
            return data.get("access_token")
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Login error: {str(e)}")
        return None

def test_sources_search(token):
    """Test academic sources search"""
    print("Testing sources search...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/sources",
            headers=headers,
            params={"query": "artificial intelligence education", "limit": 5}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"Sources search successful - Found {len(data.get('sources', []))} sources")
            return True
        else:
            print(f"Sources search failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Sources search error: {str(e)}")
        return False

def test_file_upload(token):
    """Test file upload (create a dummy PDF for testing)"""
    print("Testing file upload...")
    try:
        # Create a dummy PDF content for testing
        dummy_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test Assignment) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"
        
        headers = {"Authorization": f"Bearer {token}"}
        files = {"file": ("test_assignment.pdf", dummy_pdf_content, "application/pdf")}
        
        response = requests.post(
            f"{BASE_URL}/upload",
            headers=headers,
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"File upload successful - Assignment ID: {data.get('assignment_id')}")
            return data.get('assignment_id')
        else:
            print(f"File upload failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"File upload error: {str(e)}")
        return None

def test_analysis_retrieval(token, assignment_id):
    """Test analysis results retrieval"""
    print("Testing analysis retrieval...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/analysis/{assignment_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Analysis retrieval successful - Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"Analysis retrieval failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Analysis retrieval error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("Starting API Tests for Academic Assignment Helper")
    print("=" * 60)
    
    # Test 1: Health Check
    if not test_health_check():
        print("Health check failed. Make sure the API is running.")
        return
    
    print()
    
    # Test 2: Login
    token = test_login()
    if not token:
        print("Login failed. Make sure the database is initialized.")
        return
    
    print()
    
    # Test 3: Sources Search
    test_sources_search(token)
    print()
    
    # Test 4: File Upload
    assignment_id = test_file_upload(token)
    if assignment_id:
        print()
        # Test 5: Analysis Retrieval
        test_analysis_retrieval(token, assignment_id)
    
    print()
    print("=" * 60)
    print("API testing completed!")
    print("\nNext steps:")
    print("1. Check the n8n interface at http://localhost:5678")
    print("2. Monitor the workflow execution")
    print("3. Check the database for stored data")

if __name__ == "__main__":
    main()
