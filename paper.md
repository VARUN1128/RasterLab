# SAR Analysis Webapp: An Open-Source Tool for Interactive Synthetic Aperture Radar Data Processing

## Summary

The SAR Analysis Webapp (RasterLab) is an open-source web application designed to democratize Synthetic Aperture Radar (SAR) data processing and analysis. Built with modern web technologies, this tool provides an intuitive interface for researchers, geospatial analysts, and data scientists to process large SAR datasets through configurable tiling operations. The application addresses the critical need for accessible SAR data processing tools by offering a lightweight, browser-based solution that eliminates the complexity of traditional desktop GIS software. RasterLab enables users to upload GeoTIFF files, generate tiles with customizable dimensions and overlap parameters, and export results in multiple formats, making SAR data analysis more accessible to the broader scientific community and facilitating machine learning workflows that require systematic data preprocessing.

## Statement of Need

The processing and analysis of Synthetic Aperture Radar (SAR) data has traditionally been constrained by the complexity and cost of specialized software tools. Existing solutions such as SNAP (Sentinel Application Platform), ENVI, and ArcGIS require significant technical expertise, expensive licenses, and substantial computational resources, creating barriers for researchers and practitioners in developing countries and smaller institutions. Furthermore, the growing demand for SAR data in machine learning applications, disaster monitoring, and environmental studies necessitates tools that can efficiently preprocess large datasets into manageable tiles while maintaining geospatial accuracy.

Current open-source alternatives like QGIS, while powerful, often require extensive configuration and lack specialized workflows for SAR data tiling and preprocessing. The absence of web-based, accessible tools for SAR data processing creates a significant gap in the geospatial analysis ecosystem, particularly for users who need quick, reliable data preprocessing without the overhead of desktop software installation and configuration.

RasterLab addresses these limitations by providing a streamlined, web-based interface that simplifies SAR data processing through automated tiling operations with configurable parameters. The tool eliminates the need for complex software installation, reduces the learning curve for new users, and provides a foundation for scalable SAR data processing workflows that can be easily integrated into larger analysis pipelines.

## Functionality

### Core Features

**Data Upload and Validation**
- Support for GeoTIFF format files with automatic geospatial metadata validation
- Drag-and-drop interface with real-time file validation
- Automatic coordinate reference system (CRS) detection and transformation to WGS84 (EPSG:4326)
- File size and format validation with user-friendly error messages

**Configurable Tiling System**
- Flexible tile size configuration supporting square (256×256, 512×512, 1024×1024) and rectangular tiles
- Custom tile dimensions with user-defined width and height parameters
- Configurable overlap ratios (0-99%) for optimal data coverage and machine learning applications
- Automatic calculation of optimal tile distribution across the input raster

**Interactive Processing Pipeline**
- Real-time processing status updates with progress indicators
- Asynchronous processing to prevent browser blocking during large file operations
- Session-based tile management with unique identifiers for organized data storage
- Automatic cleanup of temporary files and session data

**Data Visualization and Export**
- Interactive results display showing original raster bounding box coordinates
- Comprehensive tile information table with geographic coordinates and metadata
- Multiple export options including individual tile downloads, bulk ZIP archives, and sample tile collections
- Metadata export in CSV and JSON formats for integration with external analysis tools

**Modern Web Interface**
- Responsive design optimized for desktop and mobile devices
- Intuitive user interface built with React and Tailwind CSS
- Real-time error handling and validation feedback
- Cross-browser compatibility with modern web standards

### Technical Architecture

**Backend (FastAPI)**
- High-performance Python web framework for rapid API development
- Rasterio library for efficient GeoTIFF processing and geospatial operations
- PyProj for coordinate reference system transformations
- Asynchronous request handling for improved scalability
- RESTful API design with comprehensive error handling

**Frontend (React)**
- Modern JavaScript framework for dynamic user interface
- Component-based architecture for maintainable code structure
- Axios for efficient HTTP client communication
- Real-time state management for responsive user experience

**Data Processing Pipeline**
- Memory-efficient raster processing using windowed operations
- Automatic CRS transformation and coordinate validation
- Optimized tile generation with configurable compression
- Session-based file management with automatic cleanup

## Installation

### Prerequisites

- **Node.js** (v14 or higher) - [Download from nodejs.org](https://nodejs.org/)
- **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)
- **Git** - [Download from git-scm.com](https://git-scm.com/)
- **Minimum 4GB RAM** (8GB+ recommended for large files)
- **2GB free disk space** for dependencies and temporary files

### Automated Installation

**Windows:**
```bash
# Clone the repository
git clone https://github.com/VARUN1128/RasterLab.git
cd RasterLab

# Run automated setup
setup.bat

# Start the application
start_application.bat
```

**macOS/Linux:**
```bash
# Clone the repository
git clone https://github.com/VARUN1128/RasterLab.git
cd RasterLab

# Make scripts executable
chmod +x setup.sh start_application.sh

# Run automated setup
./setup.sh

# Start the application
./start_application.sh
```

### Manual Installation

**Backend Setup:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start backend server
python backend/main.py
```

**Frontend Setup:**
```bash
# Install Node.js dependencies
npm install

# Start development server
npm start
```

### Verification

1. Backend should be accessible at `http://localhost:8000`
2. Frontend should be accessible at `http://localhost:3000`
3. Health check endpoint: `http://localhost:8000/health`

## Example Usage

### Basic SAR Data Processing

```python
import requests

# Upload and process a SAR GeoTIFF file
def process_sar_data(file_path, tile_size=512, overlap=0.25):
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

# Process Sentinel-1 SAR data
result = process_sar_data("sentinel1_vh.tif", tile_size=256, overlap=0.5)
print(f"Generated {result['total_tiles']} tiles")
print(f"Session ID: {result['session_id']}")
```

### Batch Processing Workflow

```python
from pathlib import Path
import requests

def batch_process_sar_files(directory, tile_size=512, overlap=0.25):
    """Process all GeoTIFF files in a directory"""
    results = []
    
    for file_path in Path(directory).glob("*.tif"):
        print(f"Processing {file_path.name}...")
        
        try:
            result = process_sar_data(str(file_path), tile_size, overlap)
            results.append({
                'file': file_path.name,
                'tiles': result['total_tiles'],
                'session_id': result['session_id']
            })
            print(f"✓ Generated {result['total_tiles']} tiles")
            
        except Exception as e:
            print(f"✗ Error processing {file_path.name}: {e}")
    
    return results

# Process multiple SAR files
sar_files = batch_process_sar_files("./sar_data/", tile_size=256)
```

### API Integration Example

```bash
# Upload SAR data via cURL
curl -X POST "http://localhost:8000/upload-geotiff" \
  -F "file=@sentinel1_data.tif" \
  -F "tile_width=512" \
  -F "tile_height=512" \
  -F "overlap=0.25"

# Download all tiles as ZIP
curl -X GET "http://localhost:8000/download-all-tiles/session_id" \
  -o "sar_tiles.zip"

# Export metadata
curl -X GET "http://localhost:8000/list-tiles/session_id" \
  -o "tiles_metadata.json"
```

### Web Interface Usage

1. **Upload Data**: Drag and drop GeoTIFF files onto the upload area
2. **Configure Parameters**: Select tile size (256×256, 512×512, 1024×1024, or custom)
3. **Set Overlap**: Choose overlap ratio (0-99%) for optimal coverage
4. **Process**: Click "Generate Tiles" to start processing
5. **Download Results**: Export individual tiles, bulk ZIP, or metadata files

## Acknowledgements

We acknowledge the open-source community and the developers of the following libraries and frameworks that made this project possible:

- **FastAPI** (Sebastian Ramirez) - High-performance web framework for building APIs
- **React** (Meta) - JavaScript library for building user interfaces
- **Rasterio** (Mapbox) - Geospatial raster I/O library for Python
- **PyProj** (Jeff Whitaker) - Python interface to PROJ library for cartographic transformations
- **Tailwind CSS** (Adam Wathan) - Utility-first CSS framework
- **NumPy** (Travis Oliphant) - Fundamental package for scientific computing
- **Uvicorn** (Encode) - Lightning-fast ASGI server implementation

Special thanks to the European Space Agency (ESA) for providing open access to Sentinel-1 SAR data, and to the geospatial community for their continued development of open-source tools that enable accessible Earth observation data analysis.

## References

```bibtex
@software{rasterlab2024,
  title={RasterLab: SAR Analysis Webapp},
  author={Varun},
  year={2024},
  url={https://github.com/VARUN1128/RasterLab},
  note={Open-source web application for Synthetic Aperture Radar data processing and tiling}
}

@article{fastapi2020,
  title={FastAPI: A modern, fast web framework for building APIs with Python 3.7+},
  author={Ramirez, Sebastian},
  journal={GitHub},
  year={2020},
  url={https://github.com/tiangolo/fastapi}
}

@article{rasterio2019,
  title={Rasterio: Geospatial raster I/O for Python programmers},
  author={Gillies, Sean and others},
  journal={GitHub},
  year={2019},
  url={https://github.com/rasterio/rasterio}
}

@article{react2013,
  title={React: A JavaScript library for building user interfaces},
  author={Walke, Jordan and others},
  journal={GitHub},
  year={2013},
  url={https://github.com/facebook/react}
}

@article{pyproj2019,
  title={PyProj: Python interface to PROJ library},
  author={Whitaker, Jeff and others},
  journal={GitHub},
  year={2019},
  url={https://github.com/pyproj4/pyproj}
}

@article{tailwind2017,
  title={Tailwind CSS: A utility-first CSS framework},
  author={Wathan, Adam and others},
  journal={GitHub},
  year={2017},
  url={https://github.com/tailwindlabs/tailwindcss}
}

@article{sentinel1,
  title={Sentinel-1: ESA's Radar Observatory Mission for GMES Operational Services},
  author={Torres, Ramon and others},
  journal={ESA Special Publication},
  volume={1322},
  year={2012},
  publisher={ESA}
}

@article{geotiff1995,
  title={GeoTIFF: A standard image file format for geographic information},
  author={Ritter, Niles and Ruth, Mike},
  journal={GeoTIFF Revision 1.0},
  year={1995},
  publisher={GeoTIFF Committee}
}

@article{epsg4326,
  title={WGS 84: World Geodetic System 1984},
  author={National Geospatial-Intelligence Agency},
  journal={EPSG Geodetic Parameter Dataset},
  year={2020},
  url={https://epsg.io/4326}
}

@article{opencv2010,
  title={OpenCV: Open Source Computer Vision Library},
  author={Bradski, Gary and Kaehler, Adrian},
  journal={GitHub},
  year={2010},
  url={https://github.com/opencv/opencv}
}
```

---

**Keywords:** Synthetic Aperture Radar, SAR, GeoTIFF, Web Application, Geospatial Analysis, Data Processing, Open Source, React, FastAPI, Remote Sensing

**Contact:** For questions, issues, or contributions, please visit the project repository at [https://github.com/VARUN1128/RasterLab](https://github.com/VARUN1128/RasterLab) or open an issue on GitHub.
