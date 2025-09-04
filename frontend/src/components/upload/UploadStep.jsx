import React from "react";

const UploadStep = ({ pdfFile, onFileChange, onUpload, isLoading, error }) => {
  return (
    <div className="text-center">
      <div className="border-2 border-dashed border-third rounded-lg p-8 mb-4">
        <input 
          type="file" 
          accept=".pdf,.docx" 
          onChange={onFileChange} 
          className="hidden" 
          id="document-upload" 
        />
        <label htmlFor="document-upload" className="cursor-pointer block">
          <div className="text-6xl text-third mb-4">📄</div>
          <p className="text-lg text-main mb-2">Click to select PDF or Word document or drag and drop</p>
          <p className="text-sm text-third">
            {pdfFile ? `Selected: ${pdfFile.name}` : 'No file selected'}
          </p>
          <p className="text-xs text-third mt-2">Supported formats: PDF (.pdf), Word (.docx)</p>
        </label>
      </div>
      
      {error && <p className="text-red-500 mb-4">{error}</p>}
      
      <button
        onClick={onUpload}
        disabled={!pdfFile || isLoading}
        className="bg-secondary text-white px-6 py-2 rounded-lg hover:bg-secondary hover:bg-opacity-80 disabled:bg-third disabled:cursor-not-allowed"
      >
        {isLoading ? "Processing..." : "Upload Document"}
      </button>
    </div>
  );
};

export default UploadStep;
