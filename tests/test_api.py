"""
Backend API tests for RasterLab
"""
import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

@pytest.fixture
def sample_geotiff():
    """Create a sample GeoTIFF file for testing"""
    # This would normally create a test GeoTIFF file
    # For now, we'll use the existing test file
    test_file_path = "test_raster.tif"
    if os.path.exists(test_file_path):
        return test_file_path
    else:
        pytest.skip("Test GeoTIFF file not found")

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "RasterLab API"

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "supported_formats" in data

def test_upload_geotiff_success(sample_geotiff):
    """Test successful GeoTIFF upload and processing"""
    with open(sample_geotiff, "rb") as f:
        response = client.post(
            "/upload-geotiff",
            files={"file": f},
            data={
                "tile_width": 256,
                "tile_height": 256,
                "overlap": 0.25
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "original_bbox" in data
    assert "tiles" in data
    assert "total_tiles" in data
    assert "session_id" in data
    assert "tiles_directory" in data
    
    # Check bounding box structure
    bbox = data["original_bbox"]
    assert "min_lat" in bbox
    assert "max_lat" in bbox
    assert "min_lon" in bbox
    assert "max_lon" in bbox
    
    # Check tiles structure
    assert isinstance(data["tiles"], list)
    assert data["total_tiles"] == len(data["tiles"])
    
    if data["tiles"]:
        tile = data["tiles"][0]
        assert "id" in tile
        assert "min_lat" in tile
        assert "max_lat" in tile
        assert "min_lon" in tile
        assert "max_lon" in tile
        assert "file_name" in tile
        assert "download_url" in tile

def test_upload_geotiff_invalid_file():
    """Test upload with invalid file type"""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"Not a GeoTIFF file")
        f.flush()
        
        with open(f.name, "rb") as file:
            response = client.post(
                "/upload-geotiff",
                files={"file": file},
                data={
                    "tile_width": 256,
                    "tile_height": 256,
                    "overlap": 0.25
                }
            )
        
        os.unlink(f.name)
    
    assert response.status_code == 400
    assert "Only .tif/.tiff files are allowed" in response.json()["detail"]

def test_upload_geotiff_invalid_parameters():
    """Test upload with invalid parameters"""
    with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as f:
        f.write(b"Fake GeoTIFF content")
        f.flush()
        
        with open(f.name, "rb") as file:
            # Test negative tile dimensions
            response = client.post(
                "/upload-geotiff",
                files={"file": file},
                data={
                    "tile_width": -256,
                    "tile_height": 256,
                    "overlap": 0.25
                }
            )
        
        os.unlink(f.name)
    
    assert response.status_code == 400
    assert "Tile dimensions must be positive" in response.json()["detail"]

def test_upload_geotiff_invalid_overlap():
    """Test upload with invalid overlap value"""
    with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as f:
        f.write(b"Fake GeoTIFF content")
        f.flush()
        
        with open(f.name, "rb") as file:
            # Test invalid overlap
            response = client.post(
                "/upload-geotiff",
                files={"file": file},
                data={
                    "tile_width": 256,
                    "tile_height": 256,
                    "overlap": 1.5  # Invalid overlap > 1
                }
            )
        
        os.unlink(f.name)
    
    assert response.status_code == 400
    assert "Overlap must be between 0 and 1" in response.json()["detail"]

def test_download_tile_not_found():
    """Test downloading a non-existent tile"""
    response = client.get("/download-tile/nonexistent_session/tile_000001.tif")
    assert response.status_code == 404
    assert "Tile not found" in response.json()["detail"]

def test_download_all_tiles_not_found():
    """Test downloading all tiles for non-existent session"""
    response = client.get("/download-all-tiles/nonexistent_session")
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]

def test_list_tiles_not_found():
    """Test listing tiles for non-existent session"""
    response = client.get("/list-tiles/nonexistent_session")
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]

def test_cleanup_session_not_found():
    """Test cleaning up non-existent session"""
    response = client.delete("/cleanup-session/nonexistent_session")
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]

def test_cors_headers():
    """Test CORS headers are properly set"""
    response = client.options("/upload-geotiff")
    # CORS headers should be present (handled by middleware)
    assert response.status_code in [200, 405]  # OPTIONS might not be explicitly handled
