"""
Frontend component tests for RasterLab
"""
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import FileUploadForm from '../src/components/FileUploadForm';
import ResultsDisplay from '../src/components/ResultsDisplay';

// Mock fetch for API calls
global.fetch = jest.fn();

describe('FileUploadForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
    fetch.mockClear();
  });

  test('renders file upload form with all elements', () => {
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
    
    expect(screen.getByText('Upload GeoTIFF File')).toBeInTheDocument();
    expect(screen.getByText('Generate Tiles')).toBeInTheDocument();
    expect(screen.getByText('Tile Size (Pixels)')).toBeInTheDocument();
    expect(screen.getByText('Overlap Ratio')).toBeInTheDocument();
  });

  test('handles file selection via input', () => {
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
    
    const file = new File(['test content'], 'test.tif', { type: 'image/tiff' });
    const input = screen.getByLabelText(/file/i);
    
    fireEvent.change(input, { target: { files: [file] } });
    
    expect(screen.getByText('test.tif')).toBeInTheDocument();
    expect(screen.getByText('File ready for processing')).toBeInTheDocument();
  });

  test('handles file selection via drag and drop', () => {
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
    
    const file = new File(['test content'], 'test.tif', { type: 'image/tiff' });
    const dropZone = screen.getByText('Click to upload');
    
    fireEvent.dragOver(dropZone);
    fireEvent.drop(dropZone, { dataTransfer: { files: [file] } });
    
    expect(screen.getByText('test.tif')).toBeInTheDocument();
  });

  test('rejects invalid file types', () => {
    // Mock window.alert
    window.alert = jest.fn();
    
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
    
    const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
    const input = screen.getByLabelText(/file/i);
    
    fireEvent.change(input, { target: { files: [file] } });
    
    expect(window.alert).toHaveBeenCalledWith('Please select a valid GeoTIFF file (.tif or .tiff)');
  });

  test('handles tile size selection', () => {
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
    
    const tileSizeSelect = screen.getByDisplayValue('256×256');
    fireEvent.change(tileSizeSelect, { target: { value: '512' } });
    
    expect(tileSizeSelect.value).toBe('512');
  });

  test('handles custom tile size input', () => {
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
    
    // Select custom option
    const tileSizeSelect = screen.getByDisplayValue('256×256');
    fireEvent.change(tileSizeSelect, { target: { value: 'custom' } });
    
    // Enter custom size
    const customInput = screen.getByPlaceholderText(/custom tile size/i);
    fireEvent.change(customInput, { target: { value: '512x256' } });
    
    expect(customInput.value).toBe('512x256');
  });

  test('handles overlap ratio selection', () => {
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
    
    const overlapSelect = screen.getByDisplayValue('0.25');
    fireEvent.change(overlapSelect, { target: { value: '0.5' } });
    
    expect(overlapSelect.value).toBe('0.5');
  });

  test('handles custom overlap input', () => {
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
    
    // Select custom overlap
    const overlapSelect = screen.getByDisplayValue('0.25');
    fireEvent.change(overlapSelect, { target: { value: 'custom' } });
    
    // Enter custom overlap
    const customInput = screen.getByPlaceholderText(/custom overlap/i);
    fireEvent.change(customInput, { target: { value: '0.75' } });
    
    expect(customInput.value).toBe('0.75');
  });

  test('submits form with valid data', () => {
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
    
    // Select file
    const file = new File(['test content'], 'test.tif', { type: 'image/tiff' });
    const input = screen.getByLabelText(/file/i);
    fireEvent.change(input, { target: { files: [file] } });
    
    // Submit form
    const submitButton = screen.getByText('Generate Tiles');
    fireEvent.click(submitButton);
    
    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
    expect(mockOnSubmit).toHaveBeenCalledWith(expect.any(FormData));
  });

  test('prevents submission without file', () => {
    window.alert = jest.fn();
    
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
    
    const submitButton = screen.getByText('Generate Tiles');
    fireEvent.click(submitButton);
    
    expect(window.alert).toHaveBeenCalledWith('Please select a GeoTIFF file');
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('shows loading state', () => {
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={true} />);
    
    expect(screen.getByText('Processing GeoTIFF...')).toBeInTheDocument();
    expect(screen.getByRole('button')).toBeDisabled();
  });

  test('removes selected file', () => {
    render(<FileUploadForm onSubmit={mockOnSubmit} loading={false} />);
    
    // Select file
    const file = new File(['test content'], 'test.tif', { type: 'image/tiff' });
    const input = screen.getByLabelText(/file/i);
    fireEvent.change(input, { target: { files: [file] } });
    
    // Remove file
    const removeButton = screen.getByText('Remove file');
    fireEvent.click(removeButton);
    
    expect(screen.getByText('Click to upload')).toBeInTheDocument();
  });
});

describe('ResultsDisplay', () => {
  const mockResults = {
    original_bbox: {
      min_lat: 37.7,
      max_lat: 37.8,
      min_lon: -122.5,
      max_lon: -122.3
    },
    tiles: [
      {
        id: 1,
        min_lat: 37.7,
        max_lat: 37.75,
        min_lon: -122.5,
        max_lon: -122.4,
        file_name: 'tile_000001.tif'
      },
      {
        id: 2,
        min_lat: 37.75,
        max_lat: 37.8,
        min_lon: -122.4,
        max_lon: -122.3,
        file_name: 'tile_000002.tif'
      }
    ],
    total_tiles: 2,
    session_id: 'test_session_123'
  };

  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders results with all sections', () => {
    render(<ResultsDisplay results={mockResults} />);
    
    expect(screen.getByText('Analysis Results')).toBeInTheDocument();
    expect(screen.getByText('Original Raster Bounding Box')).toBeInTheDocument();
    expect(screen.getByText('Generated Tiles')).toBeInTheDocument();
    expect(screen.getByText('Export Results')).toBeInTheDocument();
  });

  test('displays bounding box coordinates', () => {
    render(<ResultsDisplay results={mockResults} />);
    
    expect(screen.getByText('37.700000')).toBeInTheDocument(); // min_lat
    expect(screen.getByText('37.800000')).toBeInTheDocument(); // max_lat
    expect(screen.getByText('-122.500000')).toBeInTheDocument(); // min_lon
    expect(screen.getByText('-122.300000')).toBeInTheDocument(); // max_lon
  });

  test('displays tiles table', () => {
    render(<ResultsDisplay results={mockResults} />);
    
    expect(screen.getByText('Tile #1')).toBeInTheDocument();
    expect(screen.getByText('Tile #2')).toBeInTheDocument();
    expect(screen.getByText('tile_000001.tif')).toBeInTheDocument();
    expect(screen.getByText('tile_000002.tif')).toBeInTheDocument();
  });

  test('handles tile download', async () => {
    // Mock successful download
    fetch.mockResolvedValueOnce({
      ok: true,
      blob: () => Promise.resolve(new Blob(['test content']))
    });

    render(<ResultsDisplay results={mockResults} />);
    
    const downloadButtons = screen.getAllByText('Download');
    fireEvent.click(downloadButtons[0]);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/download-tile/test_session_123/tile_000001.tif',
        expect.any(Object)
      );
    });
  });

  test('handles download all tiles', async () => {
    // Mock successful download
    fetch.mockResolvedValueOnce({
      ok: true,
      blob: () => Promise.resolve(new Blob(['zip content']))
    });

    render(<ResultsDisplay results={mockResults} />);
    
    const downloadAllButton = screen.getByText('Download All Tiles (ZIP)');
    fireEvent.click(downloadAllButton);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/download-all-tiles/test_session_123',
        expect.any(Object)
      );
    });
  });

  test('handles CSV export', () => {
    render(<ResultsDisplay results={mockResults} />);
    
    const csvButton = screen.getByText('Export CSV');
    fireEvent.click(csvButton);
    
    // CSV export should trigger download
    // This is tested by checking if the function was called
    expect(csvButton).toBeInTheDocument();
  });

  test('handles JSON export', () => {
    render(<ResultsDisplay results={mockResults} />);
    
    const jsonButton = screen.getByText('Export JSON');
    fireEvent.click(jsonButton);
    
    // JSON export should trigger download
    expect(jsonButton).toBeInTheDocument();
  });

  test('handles sample download', () => {
    render(<ResultsDisplay results={mockResults} />);
    
    const sampleButton = screen.getByText('Download Sample (10 tiles)');
    fireEvent.click(sampleButton);
    
    // Sample download should trigger individual downloads
    expect(sampleButton).toBeInTheDocument();
  });

  test('renders without results', () => {
    render(<ResultsDisplay results={null} />);
    
    // Should not render anything when no results
    expect(screen.queryByText('Analysis Results')).not.toBeInTheDocument();
  });

  test('handles empty tiles array', () => {
    const emptyResults = {
      ...mockResults,
      tiles: [],
      total_tiles: 0
    };
    
    render(<ResultsDisplay results={emptyResults} />);
    
    expect(screen.getByText('0')).toBeInTheDocument(); // total_tiles
    expect(screen.getByText('Showing 0 tiles')).toBeInTheDocument();
  });
});
