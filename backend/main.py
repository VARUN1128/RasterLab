from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import rasterio
from rasterio.warp import transform_bounds, calculate_default_transform
from rasterio.crs import CRS
from rasterio.windows import Window
import numpy as np
import tempfile
import os
import shutil
from typing import List, Dict, Any, Tuple
import logging
from datetime import datetime

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

# Create tiles directory if it doesn't exist
TILES_DIR = "tiles"
os.makedirs(TILES_DIR, exist_ok=True)

# Mount static files for serving tiles
app.mount("/tiles", StaticFiles(directory=TILES_DIR), name="tiles")

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

def generate_tiles(file_path: str, tile_width: int, tile_height: int, overlap: float, session_id: str) -> List[Dict[str, Any]]:
    """
    Generate tiles for a raster dataset with specified size and overlap.
    Saves actual tile images to disk.
    
    Args:
        file_path: Path to the GeoTIFF file
        tile_width: Width of each tile in pixels (e.g., 512)
        tile_height: Height of each tile in pixels (e.g., 256)
        overlap: Overlap ratio between 0 and 1 (e.g., 0.5 for 50% overlap)
        session_id: Unique session identifier for organizing tiles
        
    Returns:
        List of tile dictionaries with geographic bounding boxes and file paths
        
    Raises:
        Exception: If file cannot be read or tiling fails
    """
    try:
        # Create session directory for tiles
        session_dir = os.path.join(TILES_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        with rasterio.open(file_path) as dataset:
            height, width = dataset.height, dataset.width
            transform = dataset.transform
            src_crs = dataset.crs
            
            logger.info(f"Raster dimensions: {width}x{height}")
            logger.info(f"Transform: {transform}")
            logger.info(f"CRS: {src_crs}")
            logger.info(f"Saving tiles to: {session_dir}")
            
            # Calculate step size based on tile dimensions and overlap
            step_size_x = int(tile_width * (1 - overlap))
            step_size_y = int(tile_height * (1 - overlap))
            
            # Calculate number of tiles needed
            num_tiles_x = int(np.ceil(width / step_size_x))
            num_tiles_y = int(np.ceil(height / step_size_y))
            
            logger.info(f"Generating {num_tiles_x}x{num_tiles_y} tiles with step size {step_size_x}x{step_size_y}")
            
            tiles = []
            tile_id = 1
            
            for i in range(num_tiles_x):
                for j in range(num_tiles_y):
                    # Calculate pixel window boundaries
                    col_start = i * step_size_x
                    row_start = j * step_size_y
                    col_end = min(col_start + tile_width, width)
                    row_end = min(row_start + tile_height, height)
                    
                    # Skip tiles that are too small (less than 10% of tile dimensions)
                    if (col_end - col_start) < tile_width * 0.1 or (row_end - row_start) < tile_height * 0.1:
                        continue
                    
                    # Create window for reading tile data
                    window = Window(col_start, row_start, col_end - col_start, row_end - row_start)
                    
                    # Read tile data
                    tile_data = dataset.read(window=window)
                    
                    # Calculate tile transform
                    tile_transform = rasterio.windows.transform(window, dataset.transform)
                    
                    # Save tile as GeoTIFF
                    tile_filename = f"tile_{tile_id:06d}.tif"
                    tile_path = os.path.join(session_dir, tile_filename)
                    
                    try:
                        with rasterio.open(
                            tile_path,
                            'w',
                            driver='GTiff',
                            height=tile_data.shape[1],
                            width=tile_data.shape[2],
                            count=tile_data.shape[0],
                            dtype=tile_data.dtype,
                            crs=src_crs,
                            transform=tile_transform,
                            compress='lzw'
                        ) as tile_dataset:
                            tile_dataset.write(tile_data)
                        
                        logger.info(f"Saved tile {tile_id}: {tile_filename}")
                    except Exception as e:
                        logger.error(f"Failed to save tile {tile_id}: {str(e)}")
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
                        },
                        "file_path": tile_path,
                        "file_name": tile_filename,
                        "download_url": f"/download-tile/{session_id}/{tile_filename}"
                    })
                    tile_id += 1
            
            logger.info(f"Generated {len(tiles)} tiles and saved to {session_dir}")
            return tiles
            
    except Exception as e:
        logger.error(f"Error generating tiles: {str(e)}")
        raise Exception(f"Failed to generate tiles: {str(e)}")

@app.post("/upload-geotiff")
async def upload_geotiff_file(
    file: UploadFile = File(...),
    tile_width: int = Form(256),
    tile_height: int = Form(256),
    overlap: float = Form(0.25)
):
    """
    Upload and process GeoTIFF file to generate tiles.
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.tif', '.tiff')):
            raise HTTPException(status_code=400, detail="Only .tif/.tiff files are allowed")
        
        # Validate parameters
        if tile_width <= 0 or tile_height <= 0:
            raise HTTPException(status_code=400, detail="Tile dimensions must be positive")
        
        if overlap < 0 or overlap >= 1:
            raise HTTPException(status_code=400, detail="Overlap must be between 0 and 1")
        
        # Generate unique session ID
        session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename.split('.')[0]}"
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tif') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Read raster bounds
            logger.info(f"Processing file: {file.filename}")
            original_bbox = read_raster_bounds(tmp_file_path)
            
            # Generate tiles and save them
            tiles = generate_tiles(tmp_file_path, tile_width, tile_height, overlap, session_id)
            
            return {
                "original_bbox": original_bbox,
                "tiles": tiles,
                "total_tiles": len(tiles),
                "tile_width": tile_width,
                "tile_height": tile_height,
                "overlap_ratio": overlap,
                "session_id": session_id,
                "tiles_directory": f"/tiles/{session_id}"
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

@app.get("/download-tile/{session_id}/{filename}")
async def download_tile(session_id: str, filename: str):
    """Download a specific tile file"""
    tile_path = os.path.join(TILES_DIR, session_id, filename)
    
    if not os.path.exists(tile_path):
        raise HTTPException(status_code=404, detail="Tile not found")
    
    return FileResponse(
        path=tile_path,
        filename=filename,
        media_type='image/tiff',
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/download-all-tiles/{session_id}")
async def download_all_tiles(session_id: str):
    """Download all tiles as a ZIP file"""
    import zipfile
    from io import BytesIO
    
    session_dir = os.path.join(TILES_DIR, session_id)
    
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Create ZIP file in memory
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(session_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, session_dir)
                zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    zip_content = zip_buffer.getvalue()
    
    from fastapi.responses import Response
    return Response(
        content=zip_content,
        media_type='application/zip',
        headers={
            "Content-Disposition": f"attachment; filename=tiles_{session_id}.zip",
            "Content-Length": str(len(zip_content))
        }
    )

@app.get("/list-tiles/{session_id}")
async def list_tiles(session_id: str):
    """List all tiles in a session"""
    session_dir = os.path.join(TILES_DIR, session_id)
    
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found")
    
    tiles = []
    for filename in os.listdir(session_dir):
        if filename.endswith('.tif'):
            file_path = os.path.join(session_dir, filename)
            file_size = os.path.getsize(file_path)
            tiles.append({
                "filename": filename,
                "size_bytes": file_size,
                "download_url": f"/download-tile/{session_id}/{filename}"
            })
    
    return {
        "session_id": session_id,
        "tiles": tiles,
        "total_tiles": len(tiles)
    }

@app.delete("/cleanup-session/{session_id}")
async def cleanup_session(session_id: str):
    """Clean up a session and all its tiles"""
    session_dir = os.path.join(TILES_DIR, session_id)
    
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        shutil.rmtree(session_dir)
        return {"message": f"Session {session_id} cleaned up successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cleanup session: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RasterLab API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)