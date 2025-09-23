#!/usr/bin/env python3
"""
Test the upload endpoint to create tiles
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_upload():
    """Test uploading a GeoTIFF file"""
    
    # Test file upload
    try:
        with open('test_raster.tif', 'rb') as f:
            files = {'file': ('test_raster.tif', f, 'image/tiff')}
            data = {
                'tile_size': '512',
                'overlap': '0.5'
            }
            
            print("📤 Uploading test_raster.tif...")
            response = requests.post(f"{BASE_URL}/upload-geotiff", files=files, data=data)
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Upload successful!")
                print(f"Session ID: {result.get('session_id')}")
                print(f"Total tiles: {result.get('total_tiles')}")
                print(f"Tiles directory: {result.get('tiles_directory')}")
                
                # Test download endpoints with the new session
                session_id = result.get('session_id')
                if session_id:
                    test_downloads(session_id)
            else:
                print(f"❌ Upload failed: {response.text}")
                
    except Exception as e:
        print(f"❌ Upload error: {e}")

def test_downloads(session_id):
    """Test download endpoints with a real session"""
    
    print(f"\n🔍 Testing downloads for session: {session_id}")
    
    # Test list tiles
    try:
        response = requests.get(f"{BASE_URL}/list-tiles/{session_id}")
        print(f"List tiles: {response.status_code}")
        if response.status_code == 200:
            tiles = response.json()
            print(f"Found {len(tiles)} tiles")
            if tiles:
                first_tile = tiles[0]
                print(f"First tile: {first_tile}")
                
                # Test download first tile
                tile_filename = first_tile.get('filename')
                if tile_filename:
                    print(f"\n📥 Testing download of {tile_filename}")
                    response = requests.get(f"{BASE_URL}/download-tile/{session_id}/{tile_filename}")
                    print(f"Download tile: {response.status_code}")
                    print(f"Content-Type: {response.headers.get('content-type')}")
                    if response.status_code == 200:
                        print(f"File size: {len(response.content)} bytes")
                    else:
                        print(f"Error: {response.text}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ List tiles error: {e}")
    
    # Test download all tiles
    try:
        print(f"\n📦 Testing download all tiles")
        response = requests.get(f"{BASE_URL}/download-all-tiles/{session_id}")
        print(f"Download all tiles: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        if response.status_code == 200:
            print(f"ZIP size: {len(response.content)} bytes")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Download all tiles error: {e}")

if __name__ == "__main__":
    test_upload()
