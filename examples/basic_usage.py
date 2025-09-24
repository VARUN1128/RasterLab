"""
Basic usage examples for RasterLab API
"""
import requests
import json
import os
from pathlib import Path

class RasterLabClient:
    """Simple client for RasterLab API"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self):
        """Check if the API is running"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
    
    def upload_geotiff(self, file_path, tile_width=256, tile_height=256, overlap=0.25):
        """Upload and process a GeoTIFF file"""
        url = f"{self.base_url}/upload-geotiff"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'tile_width': tile_width,
                'tile_height': tile_height,
                'overlap': overlap
            }
            
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
            return response.json()
    
    def download_tile(self, session_id, filename, output_path=None):
        """Download a specific tile"""
        url = f"{self.base_url}/download-tile/{session_id}/{filename}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        if output_path is None:
            output_path = filename
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return output_path
    
    def download_all_tiles(self, session_id, output_path=None):
        """Download all tiles as ZIP"""
        url = f"{self.base_url}/download-all-tiles/{session_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        if output_path is None:
            output_path = f"tiles_{session_id}.zip"
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return output_path
    
    def list_tiles(self, session_id):
        """List all tiles in a session"""
        url = f"{self.base_url}/list-tiles/{session_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def cleanup_session(self, session_id):
        """Clean up a session"""
        url = f"{self.base_url}/cleanup-session/{session_id}"
        
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()

def example_basic_processing():
    """Example: Basic GeoTIFF processing"""
    print("=== Basic GeoTIFF Processing Example ===")
    
    client = RasterLabClient()
    
    # Check if API is running
    if not client.health_check():
        print("ERROR: RasterLab API is not running. Please start it first.")
        return
    
    # Process a GeoTIFF file
    file_path = "test_raster.tif"
    if not os.path.exists(file_path):
        print(f"ERROR: Test file {file_path} not found")
        return
    
    print(f"Processing {file_path}...")
    result = client.upload_geotiff(file_path, tile_width=512, tile_height=512, overlap=0.25)
    
    print(f"✓ Generated {result['total_tiles']} tiles")
    print(f"✓ Session ID: {result['session_id']}")
    print(f"✓ Original bounds: {result['original_bbox']}")
    
    # Download all tiles
    zip_path = client.download_all_tiles(result['session_id'])
    print(f"✓ Downloaded all tiles to: {zip_path}")
    
    # Clean up
    client.cleanup_session(result['session_id'])
    print("✓ Session cleaned up")

def example_batch_processing():
    """Example: Batch processing multiple files"""
    print("\n=== Batch Processing Example ===")
    
    client = RasterLabClient()
    
    if not client.health_check():
        print("ERROR: RasterLab API is not running")
        return
    
    # Find all GeoTIFF files in current directory
    tif_files = list(Path('.').glob('*.tif'))
    
    if not tif_files:
        print("No GeoTIFF files found in current directory")
        return
    
    results = []
    
    for file_path in tif_files:
        print(f"Processing {file_path.name}...")
        
        try:
            result = client.upload_geotiff(
                str(file_path), 
                tile_width=256, 
                tile_height=256, 
                overlap=0.1
            )
            
            results.append({
                'file': file_path.name,
                'tiles': result['total_tiles'],
                'session_id': result['session_id']
            })
            
            print(f"  ✓ Generated {result['total_tiles']} tiles")
            
            # Download tiles
            zip_path = f"output_{file_path.stem}.zip"
            client.download_all_tiles(result['session_id'], zip_path)
            print(f"  ✓ Downloaded to {zip_path}")
            
            # Clean up
            client.cleanup_session(result['session_id'])
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print(f"\n✓ Processed {len(results)} files successfully")

def example_custom_parameters():
    """Example: Using custom tiling parameters"""
    print("\n=== Custom Parameters Example ===")
    
    client = RasterLabClient()
    
    if not client.health_check():
        print("ERROR: RasterLab API is not running")
        return
    
    file_path = "test_raster.tif"
    if not os.path.exists(file_path):
        print(f"ERROR: Test file {file_path} not found")
        return
    
    # Different parameter configurations
    configs = [
        {"name": "Small tiles, no overlap", "width": 128, "height": 128, "overlap": 0.0},
        {"name": "Medium tiles, 25% overlap", "width": 256, "height": 256, "overlap": 0.25},
        {"name": "Large tiles, 50% overlap", "width": 512, "height": 512, "overlap": 0.5},
        {"name": "Rectangular tiles", "width": 512, "height": 256, "overlap": 0.25},
    ]
    
    for config in configs:
        print(f"\nTesting: {config['name']}")
        
        result = client.upload_geotiff(
            file_path,
            tile_width=config['width'],
            tile_height=config['height'],
            overlap=config['overlap']
        )
        
        print(f"  Generated {result['total_tiles']} tiles")
        print(f"  Tile size: {config['width']}x{config['height']}")
        print(f"  Overlap: {config['overlap']*100}%")
        
        # Clean up
        client.cleanup_session(result['session_id'])

def example_metadata_export():
    """Example: Exporting metadata"""
    print("\n=== Metadata Export Example ===")
    
    client = RasterLabClient()
    
    if not client.health_check():
        print("ERROR: RasterLab API is not running")
        return
    
    file_path = "test_raster.tif"
    if not os.path.exists(file_path):
        print(f"ERROR: Test file {file_path} not found")
        return
    
    # Process file
    result = client.upload_geotiff(file_path)
    
    # Export metadata as JSON
    metadata_file = f"metadata_{result['session_id']}.json"
    with open(metadata_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✓ Metadata exported to: {metadata_file}")
    
    # Export tile list as CSV
    tile_list = client.list_tiles(result['session_id'])
    csv_file = f"tiles_{result['session_id']}.csv"
    
    with open(csv_file, 'w') as f:
        f.write("Tile ID,Filename,Size (bytes),Download URL\n")
        for tile in tile_list['tiles']:
            f.write(f"{tile['filename'].split('_')[1].split('.')[0]},{tile['filename']},{tile['size_bytes']},{tile['download_url']}\n")
    
    print(f"✓ Tile list exported to: {csv_file}")
    
    # Clean up
    client.cleanup_session(result['session_id'])

if __name__ == "__main__":
    print("RasterLab API Examples")
    print("======================")
    
    # Run examples
    example_basic_processing()
    example_batch_processing()
    example_custom_parameters()
    example_metadata_export()
    
    print("\n✓ All examples completed!")
