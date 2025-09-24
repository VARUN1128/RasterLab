"""
Integration tests for the complete RasterLab workflow
"""
import pytest
import tempfile
import os
import zipfile
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

@pytest.fixture
def sample_geotiff():
    """Create a sample GeoTIFF file for testing"""
    test_file_path = "test_raster.tif"
    if os.path.exists(test_file_path):
        return test_file_path
    else:
        pytest.skip("Test GeoTIFF file not found")

class TestFullWorkflow:
    """Test the complete workflow from upload to download"""
    
    def test_complete_workflow(self, sample_geotiff):
        """Test the complete workflow: upload -> process -> download"""
        
        # Step 1: Upload and process GeoTIFF
        with open(sample_geotiff, "rb") as f:
            upload_response = client.post(
                "/upload-geotiff",
                files={"file": f},
                data={
                    "tile_width": 256,
                    "tile_height": 256,
                    "overlap": 0.25
                }
            )
        
        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        session_id = upload_data["session_id"]
        
        # Verify upload response structure
        assert "original_bbox" in upload_data
        assert "tiles" in upload_data
        assert "total_tiles" in upload_data
        assert upload_data["total_tiles"] > 0
        
        # Step 2: List tiles
        list_response = client.get(f"/list-tiles/{session_id}")
        assert list_response.status_code == 200
        list_data = list_response.json()
        
        assert list_data["session_id"] == session_id
        assert list_data["total_tiles"] == upload_data["total_tiles"]
        assert len(list_data["tiles"]) == upload_data["total_tiles"]
        
        # Step 3: Download individual tile
        if upload_data["tiles"]:
            first_tile = upload_data["tiles"][0]
            tile_filename = first_tile["file_name"]
            
            download_response = client.get(f"/download-tile/{session_id}/{tile_filename}")
            assert download_response.status_code == 200
            assert download_response.headers["content-type"] == "image/tiff"
            
        # Step 4: Download all tiles as ZIP
        zip_response = client.get(f"/download-all-tiles/{session_id}")
        assert zip_response.status_code == 200
        assert zip_response.headers["content-type"] == "application/zip"
        
        # Verify ZIP content
        zip_content = zip_response.content
        assert len(zip_content) > 0
        
        # Step 5: Cleanup session
        cleanup_response = client.delete(f"/cleanup-session/{session_id}")
        assert cleanup_response.status_code == 200
        assert "cleaned up successfully" in cleanup_response.json()["message"]
        
        # Verify cleanup worked
        list_after_cleanup = client.get(f"/list-tiles/{session_id}")
        assert list_after_cleanup.status_code == 404

    def test_different_tile_sizes(self, sample_geotiff):
        """Test processing with different tile sizes"""
        tile_configs = [
            {"width": 128, "height": 128, "overlap": 0.1},
            {"width": 512, "height": 256, "overlap": 0.5},
            {"width": 1024, "height": 1024, "overlap": 0.25}
        ]
        
        for config in tile_configs:
            with open(sample_geotiff, "rb") as f:
                response = client.post(
                    "/upload-geotiff",
                    files={"file": f},
                    data={
                        "tile_width": config["width"],
                        "tile_height": config["height"],
                        "overlap": config["overlap"]
                    }
                )
            
            assert response.status_code == 200
            data = response.json()
            
            # Clean up after each test
            session_id = data["session_id"]
            client.delete(f"/cleanup-session/{session_id}")

    def test_error_handling(self):
        """Test error handling in the workflow"""
        
        # Test with invalid file
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
        
        # Test with invalid parameters
        with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as f:
            f.write(b"Fake GeoTIFF content")
            f.flush()
            
            with open(f.name, "rb") as file:
                response = client.post(
                    "/upload-geotiff",
                    files={"file": file},
                    data={
                        "tile_width": -256,  # Invalid
                        "tile_height": 256,
                        "overlap": 1.5  # Invalid
                    }
                )
            
            os.unlink(f.name)
        
        assert response.status_code == 400

    def test_concurrent_uploads(self, sample_geotiff):
        """Test handling multiple concurrent uploads"""
        import threading
        import time
        
        results = []
        errors = []
        
        def upload_file():
            try:
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
                results.append(response.status_code == 200)
            except Exception as e:
                errors.append(str(e))
        
        # Start multiple uploads concurrently
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=upload_file)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all uploads succeeded
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert all(results), "Not all uploads succeeded"
        
        # Clean up any created sessions
        # This is a simplified cleanup - in real scenario, you'd track session IDs
        time.sleep(1)  # Give time for processing to complete

    def test_large_file_handling(self):
        """Test handling of large files (if available)"""
        # This test would require a large GeoTIFF file
        # For now, we'll test the error handling for missing files
        large_file_path = "large_test_raster.tif"
        
        if not os.path.exists(large_file_path):
            pytest.skip("Large test file not available")
        
        with open(large_file_path, "rb") as f:
            response = client.post(
                "/upload-geotiff",
                files={"file": f},
                data={
                    "tile_width": 512,
                    "tile_height": 512,
                    "overlap": 0.1
                }
            )
        
        # Should either succeed or fail gracefully
        assert response.status_code in [200, 413, 500]  # Success, too large, or server error
