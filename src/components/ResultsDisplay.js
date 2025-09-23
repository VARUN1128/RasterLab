import React from 'react';

const ResultsDisplay = ({ results }) => {
  if (!results) return null;

  const { original_bbox, tiles, total_tiles } = results;

  const formatCoordinate = (coord) => {
    return parseFloat(coord).toFixed(6);
  };

  return (
    <div className="results-section space-y-8">
      <div className="text-center">
        <h2 className="text-4xl font-bold text-gray-900 mb-2">Analysis Results</h2>
        <p className="text-lg text-gray-600">GeoTIFF processing completed successfully</p>
      </div>
      
      {/* Original Bounding Box */}
      <div className="bg-white rounded-xl shadow-xl p-8">
        <div className="flex items-center mb-6">
          <svg className="h-8 w-8 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
          </svg>
          <h3 className="text-2xl font-bold text-gray-900">Original Raster Bounding Box</h3>
        </div>
        <div className="grid grid-cols-2 gap-6">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200">
            <div className="text-sm font-semibold text-blue-700 mb-2 uppercase tracking-wide">Min Longitude</div>
            <div className="text-2xl font-mono text-blue-900 font-bold">{formatCoordinate(original_bbox.min_lon)}</div>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200">
            <div className="text-sm font-semibold text-blue-700 mb-2 uppercase tracking-wide">Max Longitude</div>
            <div className="text-2xl font-mono text-blue-900 font-bold">{formatCoordinate(original_bbox.max_lon)}</div>
          </div>
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200">
            <div className="text-sm font-semibold text-green-700 mb-2 uppercase tracking-wide">Min Latitude</div>
            <div className="text-2xl font-mono text-green-900 font-bold">{formatCoordinate(original_bbox.min_lat)}</div>
          </div>
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200">
            <div className="text-sm font-semibold text-green-700 mb-2 uppercase tracking-wide">Max Latitude</div>
            <div className="text-2xl font-mono text-green-900 font-bold">{formatCoordinate(original_bbox.max_lat)}</div>
          </div>
        </div>
      </div>

      {/* Tiles Summary */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <svg className="h-8 w-8 text-blue-600 mr-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <h4 className="text-xl font-bold text-blue-900">Processing Complete</h4>
              <p className="text-blue-700">Successfully generated {total_tiles} tiles from your GeoTIFF</p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-blue-900">{total_tiles}</div>
            <div className="text-sm text-blue-600">Total Tiles</div>
          </div>
        </div>
      </div>

      {/* Tiles Table */}
      <div className="bg-white rounded-xl shadow-xl overflow-hidden">
        <div className="px-8 py-6 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <svg className="h-8 w-8 text-gray-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
              <h3 className="text-2xl font-bold text-gray-900">Generated Tiles</h3>
            </div>
            <div className="text-sm text-gray-600">
              Showing {tiles.length} tiles
            </div>
          </div>
        </div>
        
        <div className="tile-table max-h-96">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50 sticky top-0">
                <tr>
                  <th className="px-8 py-4 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider">
                    Tile ID
                  </th>
                  <th className="px-8 py-4 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider">
                    Min Latitude
                  </th>
                  <th className="px-8 py-4 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider">
                    Max Latitude
                  </th>
                  <th className="px-8 py-4 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider">
                    Min Longitude
                  </th>
                  <th className="px-8 py-4 text-left text-sm font-semibold text-gray-700 uppercase tracking-wider">
                    Max Longitude
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {tiles.map((tile, index) => (
                  <tr key={tile.id} className={`hover:bg-gray-50 transition-colors ${index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}`}>
                    <td className="px-8 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                          <span className="text-sm font-bold text-blue-600">{tile.id}</span>
                        </div>
                        <span className="text-sm font-semibold text-gray-900">Tile #{tile.id}</span>
                      </div>
                    </td>
                    <td className="px-8 py-4 whitespace-nowrap text-sm font-mono text-gray-600 bg-green-50">
                      {formatCoordinate(tile.min_lat)}
                    </td>
                    <td className="px-8 py-4 whitespace-nowrap text-sm font-mono text-gray-600 bg-green-50">
                      {formatCoordinate(tile.max_lat)}
                    </td>
                    <td className="px-8 py-4 whitespace-nowrap text-sm font-mono text-gray-600 bg-blue-50">
                      {formatCoordinate(tile.min_lon)}
                    </td>
                    <td className="px-8 py-4 whitespace-nowrap text-sm font-mono text-gray-600 bg-blue-50">
                      {formatCoordinate(tile.max_lon)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Export Options */}
      <div className="bg-white rounded-xl shadow-xl p-8">
        <div className="flex items-center mb-6">
          <svg className="h-8 w-8 text-purple-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 className="text-2xl font-bold text-gray-900">Export Results</h3>
        </div>
        <p className="text-gray-600 mb-6">Download your tiling results in various formats for further analysis</p>
        <div className="flex flex-wrap gap-4">
          <button
            onClick={() => {
              const csvContent = [
                'Tile ID,Min Lat,Max Lat,Min Lon,Max Lon',
                ...tiles.map(tile => 
                  `${tile.id},${tile.min_lat},${tile.max_lat},${tile.min_lon},${tile.max_lon}`
                )
              ].join('\n');
              
              const blob = new Blob([csvContent], { type: 'text/csv' });
              const url = window.URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = 'tiles.csv';
              a.click();
              window.URL.revokeObjectURL(url);
            }}
            className="inline-flex items-center px-6 py-4 border border-transparent text-lg font-semibold rounded-xl text-white bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 focus:outline-none focus:ring-4 focus:ring-green-300 transition-all duration-200 transform hover:scale-105"
          >
            <svg className="h-6 w-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export CSV
          </button>
          
          <button
            onClick={() => {
              const jsonContent = JSON.stringify(results, null, 2);
              const blob = new Blob([jsonContent], { type: 'application/json' });
              const url = window.URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = 'tiles.json';
              a.click();
              window.URL.revokeObjectURL(url);
            }}
            className="inline-flex items-center px-6 py-4 border-2 border-gray-300 text-lg font-semibold rounded-xl text-gray-700 bg-white hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-4 focus:ring-blue-300 transition-all duration-200 transform hover:scale-105"
          >
            <svg className="h-6 w-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
            Export JSON
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;
