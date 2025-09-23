from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import rasterio
from rasterio.warp import transform_bounds, calculate_default_transform
from rasterio.crs import CRS
import numpy as np
import tempfile
import os
from typing import List, Dict, Any, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RasterLab API - GeoTIFF Processing", version="2.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def read_raster_bounds(file_path: str) -> Dict[str, float]:
    """
    Read raster bounds and convert to EPSG:4326 (WGS84) if needed.
    
    Args:
        file_path: Path to the GeoTIFF file
        
    Returns:
        Dictionary with min_lat, max_lat, min_lon, max_lon in WGS84
        
    Raises:
        Exception: If file cannot be read or CRS transformation fails
    """
    try:
        with rasterio.open(file_path) as dataset:
            # Get the bounds in the original CRS
            bounds = dataset.bounds
            src_crs = dataset.crs
            
            logger.info(f"Original CRS: {src_crs}")
            logger.info(f"Original bounds: {bounds}")
            
            # If already in WGS84, return bounds directly
            if src_crs and src_crs.to_epsg() == 4326:
                return {
                    "min_lon": float(bounds.left),
                    "min_lat": float(bounds.bottom),
                    "max_lon": float(bounds.right),
                    "max_lat": float(bounds.top)
                }
            
            # Transform bounds to WGS84
            if src_crs:
                # Transform bounds from source CRS to WGS84
                min_lon, min_lat, max_lon, max_lat = transform_bounds(
                    src_crs, CRS.from_epsg(4326), *bounds
                )
                
                return {
                    "min_lon": float(min_lon),
                    "min_lat": float(min_lat),
                    "max_lon": float(max_lon),
                    "max_lat": float(max_lat)
                }
            else:
                # If no CRS information, assume it's already in WGS84
                logger.warning("No CRS information found, assuming WGS84")
                return {
                    "min_lon": float(bounds.left),
                    "min_lat": float(bounds.bottom),
                    "max_lon": float(bounds.right),
                    "max_lat": float(bounds.top)
                }
                
    except Exception as e:
        logger.error(f"Error reading raster bounds: {str(e)}")
        raise Exception(f"Failed to read raster bounds: {str(e)}")

def generate_tiles(file_path: str, tile_size: int, overlap: float) -> List[Dict[str, Any]]:
    """
    Generate tiles for a raster dataset with specified size and overlap.
    
    Args:
        file_path: Path to the GeoTIFF file
        tile_size: Size of each tile in pixels (e.g., 512)
        overlap: Overlap ratio between 0 and 1 (e.g., 0.5 for 50% overlap)
        
    Returns:
        List of tile dictionaries with geographic bounding boxes
        
    Raises:
        Exception: If file cannot be read or tiling fails
    """
    try:
        with rasterio.open(file_path) as dataset:
            height, width = dataset.height, dataset.width
            transform = dataset.transform
            src_crs = dataset.crs
            
            logger.info(f"Raster dimensions: {width}x{height}")
            logger.info(f"Transform: {transform}")
            logger.info(f"CRS: {src_crs}")
            
            # Calculate step size based on tile size and overlap
            step_size = int(tile_size * (1 - overlap))
            
            # Calculate number of tiles needed
            num_tiles_x = int(np.ceil(width / step_size))
            num_tiles_y = int(np.ceil(height / step_size))
            
            logger.info(f"Generating {num_tiles_x}x{num_tiles_y} tiles with step size {step_size}")
            
            tiles = []
            tile_id = 1
            
            for i in range(num_tiles_x):
                for j in range(num_tiles_y):
                    # Calculate pixel window boundaries
                    col_start = i * step_size
                    row_start = j * step_size
                    col_end = min(col_start + tile_size, width)
                    row_end = min(row_start + tile_size, height)
                    
                    # Skip tiles that are too small (less than 10% of tile size)
                    if (col_end - col_start) < tile_size * 0.1 or (row_end - row_start) < tile_size * 0.1:
                        continue
                    
                    # Convert pixel coordinates to geographic coordinates
                    # Get the four corners of the tile in pixel coordinates
                    pixel_corners = [
                        (col_start, row_start),  # top-left
                        (col_end, row_start),    # top-right
                        (col_end, row_end),      # bottom-right
                        (col_start, row_end)     # bottom-left
                    ]
                    
                    # Transform pixel coordinates to geographic coordinates
                    geo_coords = []
                    for col, row in pixel_corners:
                        lon, lat = rasterio.transform.xy(transform, row, col)
                        geo_coords.append((lon, lat))
                    
                    # If source CRS is not WGS84, transform coordinates
                    if src_crs and src_crs.to_epsg() != 4326:
                        from rasterio.warp import transform
                        lons, lats = zip(*geo_coords)
                        lons, lats = transform(src_crs, CRS.from_epsg(4326), lons, lats)
                        geo_coords = list(zip(lons, lats))
                    
                    # Extract bounding box from transformed coordinates
                    lons, lats = zip(*geo_coords)
                    min_lon, max_lon = min(lons), max(lons)
                    min_lat, max_lat = min(lats), max(lats)
                    
                    tiles.append({
                        "id": tile_id,
                        "min_lat": float(min_lat),
                        "max_lat": float(max_lat),
                        "min_lon": float(min_lon),
                        "max_lon": float(max_lon),
                        "pixel_bounds": {
                            "col_start": col_start,
                            "row_start": row_start,
                            "col_end": col_end,
                            "row_end": row_end
                        }
                    })
                    tile_id += 1
            
            logger.info(f"Generated {len(tiles)} tiles")
            return tiles
            
    except Exception as e:
        logger.error(f"Error generating tiles: {str(e)}")
        raise Exception(f"Failed to generate tiles: {str(e)}")

@app.post("/upload-geotiff")
async def upload_geotiff_file(
    file: UploadFile = File(...),
    tile_size: int = Form(...),
    overlap: float = Form(...)
):
    """
    Upload and process GeoTIFF file to generate tiles.
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.tif', '.tiff')):
            raise HTTPException(status_code=400, detail="Only .tif/.tiff files are allowed")
        
        # Validate parameters
        if tile_size <= 0:
            raise HTTPException(status_code=400, detail="Tile size must be positive")
        
        if overlap < 0 or overlap >= 1:
            raise HTTPException(status_code=400, detail="Overlap must be between 0 and 1")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tif') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Read raster bounds
            logger.info(f"Processing file: {file.filename}")
            original_bbox = read_raster_bounds(tmp_file_path)
            
            # Generate tiles
            tiles = generate_tiles(tmp_file_path, tile_size, overlap)
            
            return {
                "original_bbox": original_bbox,
                "tiles": tiles,
                "total_tiles": len(tiles),
                "tile_size_pixels": tile_size,
                "overlap_ratio": overlap
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "RasterLab API - GeoTIFF Processing is running",
        "version": "2.0.0",
        "supported_formats": [".tif", ".tiff"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RasterLab API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)