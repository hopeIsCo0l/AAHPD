#!/usr/bin/env python3
"""
Simple client example for Academic Assignment Helper
This script demonstrates how to use the API as an end user.
"""

import requests
import json
import time
import os

# Configuration
BASE_URL = "http://localhost:8000"
EMAIL = "test@student.com"
PASSWORD = "password123"

class AcademicHelperClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.token = None
    
    def login(self, email, password):
        """Login and get authentication token"""
        print("🔐 Logging in...")
        
        data = {
            "email": email,
            "password": password
        }
        
        response = requests.post(f"{self.base_url}/auth/login", data=data)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result["access_token"]
            print("✅ Login successful!")
            return True
        else:
            print(f"❌ Login failed: {response.text}")
            return False
    
    def search_sources(self, query, limit=5):
        """Search for academic sources"""
        print(f"🔍 Searching for sources: '{query}'")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"query": query, "limit": limit}
        
        response = requests.get(f"{self.base_url}/sources", headers=headers, params=params)
        
        if response.status_code == 200:
            result = response.json()
            sources = result["sources"]
            print(f"✅ Found {len(sources)} sources")
            
            for i, source in enumerate(sources, 1):
                print(f"\n{i}. {source['title']}")
                print(f"   Authors: {source['authors']}")
                print(f"   Type: {source['source_type']}")
                print(f"   Year: {source.get('publication_year', 'N/A')}")
                print(f"   Abstract: {source.get('abstract', 'No abstract')[:100]}...")
            
            return sources
        else:
            print(f"❌ Search failed: {response.text}")
            return []
    
    def upload_assignment(self, file_path):
        """Upload an assignment file"""
        print(f"📤 Uploading assignment: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        with open(file_path, 'rb') as f:
            files = {"file": (os.path.basename(file_path), f, "application/pdf")}
            response = requests.post(f"{self.base_url}/upload", headers=headers, files=files)
        
        if response.status_code == 200:
            result = response.json()
            assignment_id = result["assignment_id"]
            print(f"✅ Upload successful! Assignment ID: {assignment_id}")
            return assignment_id
        else:
            print(f"❌ Upload failed: {response.text}")
            return None
    
    def get_analysis(self, assignment_id):
        """Get analysis results for an assignment"""
        print(f"📊 Getting analysis for assignment {assignment_id}...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/analysis/{assignment_id}", headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("status") == "processing":
                print("⏳ Analysis is still in progress...")
                return None
            else:
                print("✅ Analysis completed!")
                self.display_analysis(result)
                return result
        else:
            print(f"❌ Failed to get analysis: {response.text}")
            return None
    
    def display_analysis(self, analysis):
        """Display analysis results in a readable format"""
        print("\n" + "="*60)
        print("📋 ASSIGNMENT ANALYSIS RESULTS")
        print("="*60)
        
        # Basic info
        print(f"📄 File: {analysis.get('filename', 'Unknown')}")
        print(f"📝 Topic: {analysis.get('topic', 'Not analyzed')}")
        print(f"🎓 Academic Level: {analysis.get('academic_level', 'Not analyzed')}")
        print(f"📊 Word Count: {analysis.get('word_count', 'Not analyzed')}")
        
        # Analysis results
        analysis_data = analysis.get('analysis', {})
        if analysis_data:
            print(f"\n🔍 PLAGIARISM ANALYSIS")
            print(f"   Score: {analysis_data.get('plagiarism_score', 'Not analyzed')}")
            print(f"   Confidence: {analysis_data.get('confidence_score', 'Not analyzed')}")
            
            print(f"\n💡 RESEARCH SUGGESTIONS")
            print(f"   {analysis_data.get('research_suggestions', 'Not analyzed')}")
            
            print(f"\n📚 CITATION RECOMMENDATIONS")
            print(f"   {analysis_data.get('citation_recommendations', 'Not analyzed')}")
            
            # Suggested sources
            sources = analysis_data.get('suggested_sources', [])
            if sources:
                print(f"\n📖 SUGGESTED SOURCES")
                for i, source in enumerate(sources, 1):
                    print(f"   {i}. {source.get('title', 'Unknown title')}")
                    print(f"      Authors: {source.get('authors', 'Unknown')}")
        
        print("="*60)
    
    def wait_for_analysis(self, assignment_id, max_wait=60):
        """Wait for analysis to complete"""
        print(f"⏳ Waiting for analysis to complete (max {max_wait}s)...")
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            result = self.get_analysis(assignment_id)
            if result and result.get("status") != "processing":
                return result
            
            print("⏳ Still processing...")
            time.sleep(5)
        
        print("⏰ Timeout waiting for analysis")
        return None

def main():
    """Main function demonstrating the client usage"""
    print("🎓 Academic Assignment Helper - Client Example")
    print("=" * 50)
    
    # Initialize client
    client = AcademicHelperClient()
    
    # Login
    if not client.login(EMAIL, PASSWORD):
        return
    
    print("\n" + "="*50)
    
    # Search for sources
    print("\n1. Searching for academic sources...")
    sources = client.search_sources("artificial intelligence education", limit=3)
    
    print("\n" + "="*50)
    
    # Upload assignment (if you have a file)
    print("\n2. Upload assignment...")
    print("   Note: Create a test PDF file or use an existing one")
    
    # Example file path - change this to your actual file
    test_file = "test_assignment.pdf"
    
    if os.path.exists(test_file):
        assignment_id = client.upload_assignment(test_file)
        
        if assignment_id:
            print("\n" + "="*50)
            print("\n3. Waiting for analysis...")
            analysis = client.wait_for_analysis(assignment_id)
            
            if analysis:
                print("\n✅ Analysis completed successfully!")
            else:
                print("\n❌ Analysis timed out or failed")
    else:
        print(f"   ⚠️  Test file '{test_file}' not found")
        print("   Create a PDF file named 'test_assignment.pdf' to test upload functionality")
    
    print("\n" + "="*50)
    print("🎉 Demo completed!")

if __name__ == "__main__":
    main()
