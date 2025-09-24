# 🌍 RasterLab - SAR Analysis Web Application

A powerful web application for processing GeoTIFF files and generating tiles with configurable size and overlap parameters. Perfect for SAR (Synthetic Aperture Radar) data analysis, satellite imagery processing, and geospatial research.

![RasterLab](https://img.shields.io/badge/Version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-red.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

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

### Development Tools
- **Node.js 14+** - JavaScript runtime
- **npm** - Package manager
- **pip** - Python package manager

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

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd "SAR Analysis webapp"
```

### Step 2: Backend Setup

1. **Navigate to the project directory**:
   ```bash
   cd "D:\SAR Analysis webapp"
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI backend**:
   ```bash
   python backend/main.py
   ```
   
   The backend will be available at `http://localhost:8000`

### Step 3: Frontend Setup

1. **Open a new terminal** and navigate to the project directory:
   ```bash
   cd "D:\SAR Analysis webapp"
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

### Step 4: Verify Installation

1. Open your browser and navigate to `http://localhost:3000`
2. You should see the RasterLab interface
3. The backend API should be accessible at `http://localhost:8000`

## 📖 Usage Guide

### Basic Workflow

1. **Access the Application**
   - Open your browser and go to `http://localhost:3000`
   - You'll see the RasterLab interface with upload form and results area

2. **Upload a GeoTIFF File**
   - Drag and drop a `.tif` or `.tiff` file onto the upload area, or
   - Click the upload area to browse and select a file
   - Supported formats: GeoTIFF files with proper geospatial metadata

3. **Configure Tiling Parameters**
   - **Tile Size**: Choose from preset sizes (256×256, 512×512, 1024×1024) or enter custom dimensions
   - **Overlap Ratio**: Set the overlap between adjacent tiles (0.0 to 0.99)
   - **Custom Dimensions**: Enter format like "512x256" for rectangular tiles

4. **Generate Tiles**
   - Click "Generate Tiles" to start processing
   - Monitor the progress indicator
   - Wait for processing to complete

5. **View and Download Results**
   - Review the original raster bounding box coordinates
   - Browse the generated tiles table
   - Download individual tiles or export all tiles as ZIP
   - Export metadata in CSV or JSON format

### Advanced Usage

#### Custom Tile Sizes
- Enter custom dimensions in the format: `width x height` (e.g., "512x256")
- For square tiles, enter just the size (e.g., "512")
- Minimum tile size: 64x64 pixels

#### Overlap Configuration
- **0.0**: No overlap between tiles
- **0.25**: 25% overlap (recommended for most use cases)
- **0.5**: 50% overlap (useful for machine learning)
- **0.75**: 75% overlap (maximum recommended overlap)

#### File Requirements
- **Format**: GeoTIFF (.tif or .tiff)
- **Coordinate System**: Any supported CRS (automatically converted to WGS84)
- **Size**: No strict limit, but larger files take longer to process
- **Bands**: Single or multi-band raster data supported

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
├── 📁 tiles/                      # Generated tile storage
│   └── 📁 {session_id}/           # Session-specific directories
│       ├── 📄 tile_000001.tif     # Individual tile files
│       ├── 📄 tile_000002.tif
│       └── 📄 ...
├── 📄 package.json                # Node.js dependencies
├── 📄 requirements.txt            # Python dependencies
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
4. Test thoroughly
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