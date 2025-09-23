# RasterLab

A web application for processing GeoTIFF files and generating tiles with configurable size and overlap parameters.

## Features

- **File Upload**: Drag and drop or click to upload GeoTIFF files
- **Configurable Tiling**: Set custom tile sizes (256×256, 512×512, 1024×1024, or custom)
- **Overlap Control**: Configure tile overlap (0.25, 0.5, 1.0, or custom)
- **Results Display**: View original bounding box and generated tiles in a responsive table
- **Export Options**: Download results as CSV or JSON
- **Modern UI**: Clean, responsive design with Tailwind CSS

## Tech Stack

### Frontend
- React 18
- Tailwind CSS
- Axios for API calls

### Backend
- Python 3.8+
- FastAPI
- Rasterio for GeoTIFF file processing
- PyProj for coordinate reference system transformations

## Setup Instructions

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8 or higher
- pip (Python package manager)

### Backend Setup

1. Navigate to the project directory:
   ```bash
   cd "D:\SAR Analysis webapp"
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI backend:
   ```bash
   python backend/main.py
   ```

   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. Start the React development server:
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Upload a GeoTIFF file by dragging and dropping or clicking the upload area
3. Select your desired tile size (in pixels) and overlap parameters
4. Click "Generate Tiles" to process the file
5. View the results including:
   - Original raster bounding box coordinates (in WGS84)
   - Generated tiles with their individual bounding boxes
6. Export the results as CSV or JSON if needed

## API Endpoints

### POST /upload-geotiff
Upload and process a GeoTIFF file to generate tiles.

**Parameters:**
- `file`: GeoTIFF file (multipart/form-data)
- `tile_size`: Integer - Size of each tile in pixels
- `overlap`: Float - Overlap ratio between 0 and 1

**Response:**
```json
{
  "original_bbox": {
    "min_lat": 37.7,
    "max_lat": 37.8,
    "min_lon": -122.5,
    "max_lon": -122.3
  },
  "tiles": [
    {
      "id": 1,
      "min_lat": 37.7,
      "max_lat": 37.8,
      "min_lon": -122.5,
      "max_lon": -122.3,
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
```

## File Structure

```
RasterLab/
├── backend/
│   └── main.py              # FastAPI backend
├── public/
│   └── index.html           # HTML template
├── src/
│   ├── components/
│   │   ├── FileUploadForm.js    # File upload component
│   │   └── ResultsDisplay.js    # Results display component
│   ├── App.js               # Main React component
│   ├── App.css              # Custom styles
│   ├── index.js             # React entry point
│   └── index.css            # Global styles
├── package.json             # Node.js dependencies
├── requirements.txt         # Python dependencies
├── tailwind.config.js       # Tailwind configuration
└── README.md               # This file
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure the backend is running on port 8000 and the frontend on port 3000
2. **File Upload Issues**: Ensure the uploaded file is a valid GeoTIFF file with proper geospatial metadata
3. **Python Dependencies**: If you encounter issues with Rasterio installation, try installing it via conda:
   ```bash
   conda install rasterio
   ```

### Dependencies Installation

If you have trouble installing Rasterio, try:
```bash
# Install conda first, then:
conda install -c conda-forge rasterio
```

## License

This project is open source and available under the MIT License.
