import React, { useState, useRef } from 'react';

const FileUploadForm = ({ onSubmit, loading }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [tileSize, setTileSize] = useState(256);
  const [overlap, setOverlap] = useState(0.25);
  const [customTileSize, setCustomTileSize] = useState('');
  const [customOverlap, setCustomOverlap] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const tileSizeOptions = [
    { value: 256, label: '256×256' },
    { value: 512, label: '512×512' },
    { value: 1024, label: '1024×1024' },
  ];

  const overlapOptions = [
    { value: 0.25, label: '0.25' },
    { value: 0.5, label: '0.5' },
    { value: 1, label: '1.0' },
  ];

  const handleFileSelect = (file) => {
    if (file && (file.name.toLowerCase().endsWith('.tif') || file.name.toLowerCase().endsWith('.tiff'))) {
      setSelectedFile(file);
    } else {
      alert('Please select a valid GeoTIFF file (.tif or .tiff)');
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleTileSizeChange = (e) => {
    const value = e.target.value;
    if (value === 'custom') {
      setCustomTileSize(tileSize.toString());
      setTileSize('');
    } else {
      setTileSize(parseInt(value));
      setCustomTileSize('');
    }
  };

  const handleOverlapChange = (e) => {
    const value = e.target.value;
    if (value === 'custom') {
      setCustomOverlap(overlap.toString());
      setOverlap('');
    } else {
      setOverlap(parseFloat(value));
      setCustomOverlap('');
    }
  };

  const handleCustomTileSizeChange = (e) => {
    const value = e.target.value;
    setCustomTileSize(value);
    if (value && !isNaN(parseInt(value)) && parseInt(value) > 0) {
      setTileSize(parseInt(value));
    }
  };

  const handleCustomOverlapChange = (e) => {
    const value = e.target.value;
    setCustomOverlap(value);
    if (value && !isNaN(parseFloat(value)) && parseFloat(value) >= 0 && parseFloat(value) < 1) {
      setOverlap(parseFloat(value));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      alert('Please select a GeoTIFF file');
      return;
    }

    if (!tileSize || tileSize <= 0) {
      alert('Please enter a valid tile size');
      return;
    }

    if (overlap < 0 || overlap >= 1) {
      alert('Overlap must be between 0 and 1');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('tile_size', tileSize);
    formData.append('overlap', overlap);

    onSubmit(formData);
  };

  const removeFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-xl p-8 sticky top-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Upload GeoTIFF File</h2>
        <p className="text-gray-600">Configure tiling parameters and upload your raster data</p>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* File Upload */}
        <div>
          <label className="block text-lg font-semibold text-gray-700 mb-4">
            GeoTIFF File
          </label>
          <div
            className={`file-upload-area relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 ${
              isDragOver ? 'dragover' : 'border-gray-300'
            } ${selectedFile ? 'border-green-400 bg-green-50' : 'hover:border-blue-400 hover:bg-blue-50'}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".tif,.tiff"
              onChange={handleFileChange}
              className="hidden"
            />
            
            {selectedFile ? (
              <div className="space-y-4">
                <div className="flex items-center justify-center">
                  <svg className="h-12 w-12 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p className="text-lg font-semibold text-green-800 mb-2">{selectedFile.name}</p>
                  <p className="text-sm text-green-600">File ready for processing</p>
                </div>
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile();
                  }}
                  className="inline-flex items-center px-4 py-2 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                >
                  <svg className="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  Remove file
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                <svg className="mx-auto h-16 w-16 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <div className="space-y-2">
                  <div className="text-lg text-gray-600">
                    <span className="font-semibold text-blue-600 hover:text-blue-500">Click to upload</span> or drag and drop
                  </div>
                  <p className="text-sm text-gray-500">GeoTIFF files only (.tif, .tiff)</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Tile Size Selection */}
        <div>
          <label className="block text-lg font-semibold text-gray-700 mb-4">
            Tile Size (Pixels)
          </label>
          <div className="space-y-3">
            <select
              value={customTileSize ? 'custom' : tileSize}
              onChange={handleTileSizeChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
            >
              {tileSizeOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
              <option value="custom">Custom Size</option>
            </select>
            
            {customTileSize !== '' && (
              <input
                type="number"
                value={customTileSize}
                onChange={handleCustomTileSizeChange}
                placeholder="Enter custom tile size in pixels"
                min="1"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
              />
            )}
            <p className="text-sm text-gray-500">Size of each tile in pixels (e.g., 512 for 512×512 tiles)</p>
          </div>
        </div>

        {/* Overlap Selection */}
        <div>
          <label className="block text-lg font-semibold text-gray-700 mb-4">
            Overlap Ratio
          </label>
          <div className="space-y-3">
            <select
              value={customOverlap ? 'custom' : overlap}
              onChange={handleOverlapChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
            >
              {overlapOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label} ({Math.round(option.value * 100)}%)
                </option>
              ))}
              <option value="custom">Custom Ratio</option>
            </select>
            
            {customOverlap !== '' && (
              <input
                type="number"
                value={customOverlap}
                onChange={handleCustomOverlapChange}
                placeholder="Enter custom overlap (0-1)"
                min="0"
                max="0.99"
                step="0.01"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
              />
            )}
            <p className="text-sm text-gray-500">Overlap between adjacent tiles (0 = no overlap, 1 = 100% overlap)</p>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || !selectedFile}
          className="w-full flex justify-center items-center py-4 px-6 border border-transparent rounded-xl shadow-lg text-lg font-semibold text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 disabled:transform-none"
        >
          {loading ? (
            <div className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing GeoTIFF...
            </div>
          ) : (
            <div className="flex items-center">
              <svg className="h-6 w-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Generate Tiles
            </div>
          )}
        </button>
      </form>
    </div>
  );
};

export default FileUploadForm;
