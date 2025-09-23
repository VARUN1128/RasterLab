#!/usr/bin/env python3
"""
Simple test script to verify the backend API is working correctly.
"""

import requests
import json

def test_backend():
    """Test the RasterLab backend API endpoints."""
    base_url = "http://localhost:8000"
    
    try:
        # Test root endpoint
        print("Testing RasterLab API...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✓ RasterLab API is running")
            print(f"Response: {response.json()}")
        else:
            print(f"✗ API endpoint failed: {response.status_code}")
            return False
        
        print("\nRasterLab backend is running correctly!")
        print("Supported file formats: .tif, .tiff")
        print("You can now start the frontend with: npm start")
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Backend is not running. Please start it first with:")
        print("python backend/main.py")
        return False
    except Exception as e:
        print(f"✗ Error testing backend: {e}")
        return False

if __name__ == "__main__":
    print("RasterLab API Test")
    print("=" * 20)
    test_backend()
