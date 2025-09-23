#!/usr/bin/env python3
"""
Test script to verify download endpoints are working
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Test all download endpoints"""
    
    # Test if backend is running
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Backend is running: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Backend not running: {e}")
        return
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test list tiles endpoint (if you have a session)
    # Replace with actual session_id from your upload
    session_id = "20241220_123456_yourfile"  # Replace with actual session ID
    
    try:
        response = requests.get(f"{BASE_URL}/list-tiles/{session_id}")
        print(f"✅ List tiles: {response.status_code}")
        if response.status_code == 200:
            print(f"Tiles: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ List tiles failed: {e}")
    
    # Test download tile endpoint (if you have a session and tile)
    tile_filename = "tile_1.tif"  # Replace with actual tile filename
    
    try:
        response = requests.get(f"{BASE_URL}/download-tile/{session_id}/{tile_filename}")
        print(f"✅ Download tile: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Content-Length: {response.headers.get('content-length')}")
        if response.status_code == 200:
            print(f"File size: {len(response.content)} bytes")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Download tile failed: {e}")
    
    # Test download all tiles endpoint
    try:
        response = requests.get(f"{BASE_URL}/download-all-tiles/{session_id}")
        print(f"✅ Download all tiles: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        if response.status_code == 200:
            print(f"ZIP size: {len(response.content)} bytes")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Download all tiles failed: {e}")

if __name__ == "__main__":
    test_endpoints()
