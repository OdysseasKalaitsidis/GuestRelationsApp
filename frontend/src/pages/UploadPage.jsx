// src/pages/UploadPage.jsx
import React, { useState } from "react";
import { completeWorkflow } from "../services/api";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [workflowResult, setWorkflowResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setError(null);
    } else {
      setError("Please select a valid PDF file");
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setLoading(true);
    setError(null);
    setWorkflowResult(null);
    
    try {
      const result = await completeWorkflow(file);
      setWorkflowResult(result);
    } catch (err) {
      console.error("Workflow failed:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setWorkflowResult(null);
    setError(null);
  };

  const getStepIcon = (status) => {
    if (status === "success") return "✅";
    if (status === "error") return "❌";
    return "⏳";
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">PDF Upload & Processing</h1>
        <p className="text-gray-600">Upload a PDF to automatically extract cases, generate AI feedback, and create followups</p>
      </div>

      {!workflowResult ? (
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="space-y-6">
            {/* File Upload Area */}
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
              <input
                type="file"
                accept="application/pdf"
                onChange={handleFileChange}
                className="hidden"
                id="pdf-upload"
              />
              <label
                htmlFor="pdf-upload"
                className="cursor-pointer block"
              >
                <div className="text-gray-600 mb-4">
                  <svg className="mx-auto h-16 w-16 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
                <span className="text-lg font-medium text-blue-600 hover:text-blue-500">
                  {file ? file.name : "Choose PDF file"}
                </span>
                {!file && <p className="text-sm text-gray-500 mt-2">or drag and drop</p>}
              </label>
            </div>

            {/* File Info */}
            {file && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <svg className="w-5 h-5 text-blue-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                    <span className="text-blue-800">
                      Selected: <span className="font-medium">{file.name}</span> 
                      ({(file.size / 1024 / 1024).toFixed(2)} MB)
                    </span>
                  </div>
                  <button
                    onClick={handleReset}
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    Change File
                  </button>
                </div>
              </div>
            )}

            {/* Upload Button */}
            {file && (
              <div className="text-center">
                <button
                  onClick={handleUpload}
                  disabled={loading}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-8 py-3 rounded-lg font-medium text-lg transition-colors disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <div className="flex items-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Processing...
                    </div>
                  ) : (
                    "Start Complete Workflow"
                  )}
                </button>
              </div>
            )}

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Error</h3>
                    <p className="text-sm text-red-700 mt-1">{error}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Success Summary */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
            <div className="text-center">
              <svg className="mx-auto h-12 w-12 text-green-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="text-lg font-medium text-green-800 mb-2">
                {workflowResult.final_message}
              </h3>
              <div className="grid grid-cols-2 gap-4 text-sm max-w-md mx-auto">
                <div className="bg-white rounded-lg p-3 border border-green-200">
                  <span className="font-medium text-green-800">Cases Created:</span>
                  <div className="text-2xl font-bold text-green-600">{workflowResult.cases_created}</div>
                </div>
                <div className="bg-white rounded-lg p-3 border border-green-200">
                  <span className="font-medium text-green-800">Followups Created:</span>
                  <div className="text-2xl font-bold text-green-600">{workflowResult.followups_created}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Workflow Steps */}
          <div>
            <h4 className="font-medium text-gray-900 mb-4 text-lg">Workflow Steps:</h4>
            <div className="space-y-3">
              {workflowResult.steps.map((step, index) => (
                <div
                  key={index}
                  className={`flex items-center p-4 rounded-lg border ${
                    step.status === "success" ? "bg-green-50 border-green-200" :
                    step.status === "error" ? "bg-red-50 border-red-200" :
                    "bg-gray-50 border-gray-200"
                  }`}
                >
                  <span className="mr-4 text-2xl">{getStepIcon(step.status)}</span>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{step.step}</p>
                    <p className="text-sm text-gray-600 mt-1">{step.message}</p>
                    {Object.keys(step.data).length > 0 && (
                      <div className="text-xs text-gray-500 mt-2 flex flex-wrap gap-2">
                        {Object.entries(step.data).map(([key, value]) => (
                          <span key={key} className="bg-white px-2 py-1 rounded border">
                            {key}: {value}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-center gap-4 mt-8 pt-6 border-t">
            <button
              onClick={handleReset}
              className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-2 rounded-lg font-medium transition-colors"
            >
              Upload Another PDF
            </button>
            <a
              href="/cases"
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
            >
              View Cases
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
