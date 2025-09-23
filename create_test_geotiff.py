#!/usr/bin/env python3
"""
Create a simple test GeoTIFF file for testing
"""

import rasterio
import numpy as np
from rasterio.transform import from_bounds
import os

def create_test_geotiff():
    """Create a simple test GeoTIFF file"""
    
    # Create a simple 1000x1000 raster
    width, height = 1000, 1000
    data = np.random.randint(0, 255, (1, height, width), dtype=np.uint8)
    
    # Define bounds (simple lat/lon bounds)
    west, south, east, north = -74.0, 40.0, -73.0, 41.0
    
    # Create transform
    transform = from_bounds(west, south, east, north, width, height)
    
    # Create the GeoTIFF file
    with rasterio.open(
        'test_raster.tif',
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=data.dtype,
        crs='EPSG:4326',
        transform=transform,
        compress='lzw'
    ) as dst:
        dst.write(data)
    
    print("✅ Created test_raster.tif")
    print(f"Size: {width}x{height}")
    print(f"Bounds: {west}, {south}, {east}, {north}")
    print(f"File size: {os.path.getsize('test_raster.tif')} bytes")

if __name__ == "__main__":
    create_test_geotiff()
