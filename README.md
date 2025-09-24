# 🌍 RasterLab - SAR Analysis Web Application

A powerful web application for processing GeoTIFF files and generating tiles with configurable size and overlap parameters. Perfect for SAR (Synthetic Aperture Radar) data analysis, satellite imagery processing, and geospatial research.

![RasterLab](https://img.shields.io/badge/Version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-red.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

Get RasterLab running in 3 simple steps:

```bash
# 1. Clone and navigate to project
git clone <repository-url>
cd "SAR Analysis webapp"

# 2. Install dependencies (run in separate terminals)
pip install -r requirements.txt
npm install

# 3. Start the application
python backend/main.py    # Terminal 1 - Backend (port 8000)
npm start                 # Terminal 2 - Frontend (port 3000)
```

Open `http://localhost:3000` in your browser and start processing GeoTIFF files!

## 🎯 Overview

RasterLab is a comprehensive web application designed for geospatial data processing, specifically optimized for SAR analysis workflows. It provides an intuitive interface for uploading GeoTIFF files and automatically generating tiles with customizable parameters, making it ideal for:

- **SAR Data Analysis**: Process Synthetic Aperture Radar imagery
- **Satellite Imagery Processing**: Handle large satellite datasets
- **Geospatial Research**: Analyze geographic data with precision
- **Machine Learning Pipelines**: Prepare data for ML model training
- **GIS Applications**: Support various Geographic Information System workflows

## ✨ Key Features

### 🚀 Core Functionality
- **📁 Drag & Drop Upload**: Intuitive file upload with visual feedback
- **⚙️ Configurable Tiling**: Custom tile sizes (256×256, 512×512, 1024×1024, or custom dimensions)
- **🔗 Overlap Control**: Precise overlap configuration (0-100% overlap between tiles)
- **💾 Automatic Storage**: Organized tile storage with session management
- **🌐 Coordinate Transformation**: Automatic conversion to WGS84 (EPSG:4326)

### 📊 Advanced Features
- **📈 Real-time Processing**: Live progress updates during file processing
- **🗺️ Bounding Box Display**: Visual representation of original raster extent
- **📋 Detailed Results**: Comprehensive tile information with geographic coordinates
- **⬇️ Multiple Download Options**:
  - Individual tile downloads
  - Bulk ZIP download of all tiles
  - Sample tile downloads (first 10 tiles)
  - Metadata export (CSV/JSON formats)

### 🎨 User Experience
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🎯 Modern UI**: Clean, intuitive interface built with Tailwind CSS
- **⚡ Fast Processing**: Optimized algorithms for quick tile generation
- **🔍 Error Handling**: Comprehensive error messages and validation

## 🛠️ Technology Stack

### Frontend
- **React 18.2.0** - Modern UI framework
- **Tailwind CSS 3.3.0** - Utility-first CSS framework
- **Axios 1.4.0** - HTTP client for API communication
- **Modern JavaScript (ES6+)** - Latest JavaScript features

### Backend
- **Python 3.8+** - Core programming language
- **FastAPI 0.100.0** - High-performance web framework
- **Rasterio 1.3.8** - Geospatial raster I/O library
- **PyProj 3.6.0** - Coordinate reference system transformations
- **NumPy 1.24.3** - Numerical computing
- **Uvicorn 0.22.0** - ASGI server

### Testing
- **Jest** - JavaScript testing framework
- **React Testing Library** - React component testing
- **Pytest** - Python testing framework
- **FastAPI TestClient** - API testing

## 📋 Prerequisites

Before installing RasterLab, ensure you have the following installed on your system:

### Required Software
- **Node.js** (v14 or higher) - [Download here](https://nodejs.org/)
- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **pip** - Usually comes with Python
- **Git** - [Download here](https://git-scm.com/)

### System Requirements
- **RAM**: Minimum 4GB (8GB+ recommended for large files)
- **Storage**: At least 2GB free space for dependencies and temporary files
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

## 🚀 Installation & Setup

### Method 1: Automated Setup (Recommended)

We provide automated setup scripts for easy installation:

#### Windows
```bash
# Run the automated setup script
.\setup.bat

# Or manually run individual scripts
.\install_dependencies.bat
.\start_application.bat
```

#### macOS/Linux
```bash
# Make scripts executable
chmod +x setup.sh install_dependencies.sh start_application.sh

# Run the automated setup script
./setup.sh

# Or manually run individual scripts
./install_dependencies.sh
./start_application.sh
```

### Method 2: Manual Setup

#### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd "SAR Analysis webapp"
```

#### Step 2: Backend Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI backend**:
   ```bash
   python backend/main.py
   ```
   
   The backend will be available at `http://localhost:8000`

#### Step 3: Frontend Setup

1. **Open a new terminal** and navigate to the project directory:
   ```bash
   cd "SAR Analysis webapp"
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the React development server**:
   ```bash
   npm start
   ```
   
   The frontend will be available at `http://localhost:3000`

#### Step 4: Verify Installation

1. Open your browser and navigate to `http://localhost:3000`
2. You should see the RasterLab interface
3. The backend API should be accessible at `http://localhost:8000`

## 📖 Usage Examples

### Example 1: Basic SAR Data Processing

```bash
# 1. Start the application
python backend/main.py    # Terminal 1
npm start                 # Terminal 2

# 2. Open browser to http://localhost:3000
# 3. Upload a SAR GeoTIFF file (e.g., Sentinel-1 data)
# 4. Configure parameters:
#    - Tile Size: 512x512
#    - Overlap: 0.25 (25%)
# 5. Click "Generate Tiles"
# 6. Download results as ZIP or individual tiles
```

### Example 2: Custom Tile Configuration

```bash
# For rectangular tiles (useful for specific ML models)
# Tile Size: 512x256
# Overlap: 0.5 (50% overlap for better ML training)

# For high-resolution analysis
# Tile Size: 1024x1024
# Overlap: 0.1 (10% overlap for efficiency)
```

### Example 3: API Usage with cURL

```bash
# Upload and process a GeoTIFF file
curl -X POST "http://localhost:8000/upload-geotiff" \
  -F "file=@sample_data.tif" \
  -F "tile_width=512" \
  -F "tile_height=512" \
  -F "overlap=0.25"

# Download all tiles as ZIP
curl -X GET "http://localhost:8000/download-all-tiles/session_id" \
  -o "tiles.zip"

# List tiles in a session
curl -X GET "http://localhost:8000/list-tiles/session_id"
```

### Example 4: Python API Client

```python
import requests
import json

# Upload and process file
def process_geotiff(file_path, tile_size=512, overlap=0.25):
    url = "http://localhost:8000/upload-geotiff"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'tile_width': tile_size,
            'tile_height': tile_size,
            'overlap': overlap
        }
        
        response = requests.post(url, files=files, data=data)
        return response.json()

# Usage
result = process_geotiff("sample_data.tif", tile_size=256, overlap=0.5)
print(f"Generated {result['total_tiles']} tiles")
print(f"Session ID: {result['session_id']}")
```

### Example 5: Batch Processing Script

```python
import os
import requests
from pathlib import Path

def batch_process_geotiffs(directory, tile_size=512, overlap=0.25):
    """Process all GeoTIFF files in a directory"""
    results = []
    
    for file_path in Path(directory).glob("*.tif"):
        print(f"Processing {file_path.name}...")
        
        try:
            result = process_geotiff(str(file_path), tile_size, overlap)
            results.append({
                'file': file_path.name,
                'tiles': result['total_tiles'],
                'session_id': result['session_id']
            })
            print(f"✓ Generated {result['total_tiles']} tiles")
            
        except Exception as e:
            print(f"✗ Error processing {file_path.name}: {e}")
    
    return results

# Usage
results = batch_process_geotiffs("./data/", tile_size=256)
```

## 🧪 Testing

### Running Tests

#### Frontend Tests
```bash
# Run all frontend tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Run specific test file
npm test -- --testNamePattern="FileUploadForm"
```

#### Backend Tests
```bash
# Run all backend tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=backend

# Run specific test file
pytest tests/test_api.py

# Run tests in parallel
pytest -n auto
```

#### Integration Tests
```bash
# Run full integration test suite
pytest tests/integration/

# Test with sample data
pytest tests/integration/ --sample-data
```

### Test Coverage

```bash
# Generate coverage report for frontend
npm test -- --coverage --watchAll=false

# Generate coverage report for backend
pytest --cov=backend --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

### Test Examples

#### Frontend Component Test
```javascript
// tests/components/FileUploadForm.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import FileUploadForm from '../../src/components/FileUploadForm';

test('renders file upload form', () => {
  render(<FileUploadForm onSubmit={jest.fn()} loading={false} />);
  
  expect(screen.getByText('Upload GeoTIFF File')).toBeInTheDocument();
  expect(screen.getByText('Generate Tiles')).toBeInTheDocument();
});

test('handles file selection', () => {
  const mockOnSubmit = jest.fn();
  render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
  
  const file = new File(['test'], 'test.tif', { type: 'image/tiff' });
  const input = screen.getByLabelText(/file/i);
  
  fireEvent.change(input, { target: { files: [file] } });
  expect(screen.getByText('test.tif')).toBeInTheDocument();
});
```

#### Backend API Test
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_upload_geotiff():
    with open("test_data/sample.tif", "rb") as f:
        response = client.post(
            "/upload-geotiff",
            files={"file": f},
            data={"tile_width": 256, "tile_height": 256, "overlap": 0.25}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "tiles" in data
    assert "session_id" in data
    assert data["total_tiles"] > 0
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### POST /upload-geotiff
Upload and process a GeoTIFF file to generate tiles.

**Request Parameters:**
- `file` (multipart/form-data): GeoTIFF file
- `tile_width` (int): Width of each tile in pixels (default: 256)
- `tile_height` (int): Height of each tile in pixels (default: 256)
- `overlap` (float): Overlap ratio between 0 and 1 (default: 0.25)

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
      },
      "file_name": "tile_000001.tif",
      "download_url": "/download-tile/session_id/tile_000001.tif"
    }
  ],
  "total_tiles": 1,
  "tile_width": 512,
  "tile_height": 512,
  "overlap_ratio": 0.25,
  "session_id": "20250115_143022_example",
  "tiles_directory": "/tiles/20250115_143022_example"
}
```

#### GET /download-tile/{session_id}/{filename}
Download a specific tile file.

**Parameters:**
- `session_id` (string): Session identifier
- `filename` (string): Tile filename

**Response:** Binary file download

#### GET /download-all-tiles/{session_id}
Download all tiles in a session as a ZIP file.

**Parameters:**
- `session_id` (string): Session identifier

**Response:** ZIP file download

#### GET /list-tiles/{session_id}
List all tiles in a session with file information.

**Parameters:**
- `session_id` (string): Session identifier

**Response:**
```json
{
  "session_id": "20250115_143022_example",
  "tiles": [
    {
      "filename": "tile_000001.tif",
      "size_bytes": 1024000,
      "download_url": "/download-tile/session_id/tile_000001.tif"
    }
  ],
  "total_tiles": 1
}
```

#### DELETE /cleanup-session/{session_id}
Clean up a session and delete all associated tile files.

**Parameters:**
- `session_id` (string): Session identifier

**Response:**
```json
{
  "message": "Session 20250115_143022_example cleaned up successfully"
}
```

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "RasterLab API"
}
```

## 📁 Project Structure

```
SAR Analysis webapp/
├── 📁 backend/
│   └── 📄 main.py                 # FastAPI backend server
├── 📁 src/
│   ├── 📁 components/
│   │   ├── 📄 FileUploadForm.js   # File upload component
│   │   └── 📄 ResultsDisplay.js   # Results display component
│   ├── 📄 App.js                  # Main React application
│   ├── 📄 App.css                 # Application styles
│   ├── 📄 index.js                # React entry point
│   └── 📄 index.css               # Global styles
├── 📁 public/
│   └── 📄 index.html              # HTML template
├── 📁 tests/                      # Test files
│   ├── 📁 frontend/               # Frontend tests
│   ├── 📁 backend/                # Backend tests
│   └── 📁 integration/            # Integration tests
├── 📁 tiles/                      # Generated tile storage
│   └── 📁 {session_id}/           # Session-specific directories
│       ├── 📄 tile_000001.tif     # Individual tile files
│       ├── 📄 tile_000002.tif
│       └── 📄 ...
├── 📁 scripts/                    # Setup and utility scripts
│   ├── 📄 setup.bat              # Windows setup script
│   ├── 📄 setup.sh               # Unix setup script
│   ├── 📄 install_dependencies.bat
│   └── 📄 start_application.bat
├── 📄 package.json                # Node.js dependencies
├── 📄 requirements.txt            # Python dependencies
├── 📄 pytest.ini                 # Pytest configuration
├── 📄 tailwind.config.js          # Tailwind CSS configuration
├── 📄 postcss.config.js           # PostCSS configuration
├── 📄 start_backend.bat           # Windows backend startup script
├── 📄 start_frontend.bat          # Windows frontend startup script
├── 📄 test_raster.tif             # Sample test file
└── 📄 README.md                   # This documentation
```

## 🔧 Troubleshooting

### Common Issues

#### 1. CORS Errors
**Problem**: Frontend cannot connect to backend
**Solution**: 
- Ensure backend is running on port 8000
- Ensure frontend is running on port 3000
- Check that CORS middleware is properly configured

#### 2. File Upload Issues
**Problem**: File upload fails or file is rejected
**Solutions**:
- Ensure file is a valid GeoTIFF (.tif or .tiff)
- Check that file has proper geospatial metadata
- Verify file is not corrupted
- Try with a smaller file first

#### 3. Python Dependencies Issues
**Problem**: Rasterio installation fails
**Solutions**:
```bash
# Option 1: Use conda (recommended)
conda install -c conda-forge rasterio

# Option 2: Install system dependencies first
# On Ubuntu/Debian:
sudo apt-get install gdal-bin libgdal-dev
pip install rasterio

# On Windows:
# Download GDAL wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
pip install GDAL-*.whl
pip install rasterio
```

#### 4. Memory Issues
**Problem**: Out of memory errors with large files
**Solutions**:
- Increase system RAM
- Process smaller sections of large files
- Use smaller tile sizes
- Close other applications

#### 5. Port Already in Use
**Problem**: Port 3000 or 8000 is already in use
**Solutions**:
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different ports
# Backend: python backend/main.py --port 8001
# Frontend: set PORT=3001 && npm start
```

### Performance Optimization

#### For Large Files
- Use smaller tile sizes (256x256 or 512x512)
- Reduce overlap ratio
- Ensure sufficient RAM (8GB+ recommended)
- Use SSD storage for better I/O performance

#### For Better Processing Speed
- Close unnecessary applications
- Use faster CPU (multi-core recommended)
- Ensure adequate cooling for sustained processing

## 🤝 Contributing

We welcome contributions to RasterLab! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `npm test && pytest`
5. Submit a pull request

### Areas for Contribution
- **Frontend**: UI/UX improvements, new features
- **Backend**: Performance optimizations, new endpoints
- **Documentation**: Better guides, examples
- **Testing**: Unit tests, integration tests
- **Bug Fixes**: Report and fix issues

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ESLint configuration
- **CSS**: Follow Tailwind CSS conventions

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:

1. **Check the Troubleshooting section** above
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Include system information** (OS, Python version, Node.js version)
5. **Provide error messages** and steps to reproduce

## 🙏 Acknowledgments

- **Rasterio** - For excellent geospatial raster I/O capabilities
- **FastAPI** - For the high-performance web framework
- **React** - For the modern UI framework
- **Tailwind CSS** - For the utility-first CSS framework
- **PyProj** - For coordinate reference system transformations

---

**Made with ❤️ for the geospatial community**

*RasterLab - Simplifying SAR data analysis and geospatial processing*