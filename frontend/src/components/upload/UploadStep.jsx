import React from "react";

const UploadStep = ({ pdfFile, onFileChange, onUpload, isLoading, error }) => {
  return (
    <div className="text-center">
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 mb-4">
        <input 
          type="file" 
          accept=".pdf,.docx" 
          onChange={onFileChange} 
          className="hidden" 
          id="document-upload" 
        />
        <label htmlFor="document-upload" className="cursor-pointer block">
          <div className="text-6xl text-gray-400 mb-4">📄</div>
          <p className="text-lg text-gray-600 mb-2">Click to select PDF or Word document or drag and drop</p>
          <p className="text-sm text-gray-500">
            {pdfFile ? `Selected: ${pdfFile.name}` : 'No file selected'}
          </p>
          <p className="text-xs text-gray-400 mt-2">Supported formats: PDF (.pdf), Word (.docx)</p>
        </label>
      </div>
      
      {error && <p className="text-red-500 mb-4">{error}</p>}
      
      <button
        onClick={onUpload}
        disabled={!pdfFile || isLoading}
        className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
      >
        {isLoading ? "Processing..." : "Upload Document"}
      </button>
    </div>
  );
};

export default UploadStep;
