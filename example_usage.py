#!/usr/bin/env python3
"""
Example script demonstrating how to use the SAR Analysis API for GeoTIFF processing.
"""

import requests
import json

def test_geotiff_upload():
    """Test uploading a GeoTIFF file to the API."""
    
    # Example API call (you would need an actual GeoTIFF file)
    api_url = "http://localhost:8000/upload-geotiff"
    
    # Example parameters
    params = {
        'tile_size': 512,
        'overlap': 0.5
    }
    
    # Example file upload (replace with actual file path)
    # files = {'file': open('example.tif', 'rb')}
    
    print("Example API usage:")
    print(f"URL: {api_url}")
    print(f"Parameters: {params}")
    print("\nTo test with a real file:")
    print("1. Start the backend: python backend/main.py")
    print("2. Use the web interface at http://localhost:3000")
    print("3. Or use curl:")
    print(f"curl -X POST '{api_url}' -F 'file=@your_file.tif' -F 'tile_size=512' -F 'overlap=0.5'")

def show_api_response_format():
    """Show the expected API response format."""
    
    example_response = {
        "original_bbox": {
            "min_lat": 37.7749,
            "max_lat": 37.7849,
            "min_lon": -122.4194,
            "max_lon": -122.4094
        },
        "tiles": [
            {
                "id": 1,
                "min_lat": 37.7749,
                "max_lat": 37.7849,
                "min_lon": -122.4194,
                "max_lon": -122.4094,
                "pixel_bounds": {
                    "col_start": 0,
                    "row_start": 0,
                    "col_end": 512,
                    "row_end": 512
                }
            }
        ],
        "total_tiles": 1,
        "tile_size_pixels": 512,
        "overlap_ratio": 0.5
    }
    
    print("\nExpected API Response Format:")
    print(json.dumps(example_response, indent=2))

if __name__ == "__main__":
    print("RasterLab API - GeoTIFF Processing Example")
    print("=" * 50)
    
    test_geotiff_upload()
    show_api_response_format()
    
    print("\nKey Features:")
    print("- Processes GeoTIFF files (.tif, .tiff)")
    print("- Automatic CRS transformation to WGS84")
    print("- Pixel-based tiling with configurable overlap")
    print("- Returns geographic bounding boxes for each tile")
    print("- Includes pixel coordinate information")
