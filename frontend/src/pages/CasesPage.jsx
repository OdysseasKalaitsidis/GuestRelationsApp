import React, { useState, useEffect } from 'react';
import CasesTable from '../components/CasesTable';
import UploadModal from '../components/UploadModal';
import { fetchCasesWithFollowups } from '../services/api';

const CasesPage = () => {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showUploadModal, setShowUploadModal] = useState(false);

  const loadCases = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const data = await fetchCasesWithFollowups();
      setCases(data);
    } catch (err) {
      console.error('Failed to load cases:', err);
      setError(`Failed to load cases: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCases();
  }, []);

  const handleWorkflowComplete = () => {
    // Refresh the cases list after workflow completion
    loadCases();
  };

  const handleOpenUploadModal = () => {
    setShowUploadModal(true);
  };

  const handleCloseUploadModal = () => {
    setShowUploadModal(false);
  };

  const handleClearAllData = async () => {
    if (window.confirm("Are you sure you want to clear all data? This action cannot be undone.")) {
      try {
        const response = await fetch('/api/documents/clear-all-data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (response.ok) {
          alert('All data cleared successfully!');
          loadCases(); // Refresh the cases list
        } else {
          throw new Error('Failed to clear data');
        }
      } catch (err) {
        console.error('Failed to clear data:', err);
        alert('Failed to clear data. Please try again.');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading cases...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <p className="text-red-600 text-lg mb-4">{error}</p>
          <button
            onClick={loadCases}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Cases Management</h1>
          <p className="text-gray-600">
            View and manage all cases with their associated followups
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={handleOpenUploadModal}
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors flex items-center space-x-2"
          >
            <span>📄</span>
            <span>Start New Workflow</span>
          </button>
          <button
            onClick={handleClearAllData}
            className="bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600 transition-colors flex items-center space-x-2"
          >
            <span>🗑️</span>
            <span>Clear All Data</span>
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <span className="text-2xl">📋</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Cases</p>
              <p className="text-2xl font-bold text-gray-900">{cases.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <span className="text-2xl">⏳</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">In Progress</p>
              <p className="text-2xl font-bold text-gray-900">
                {cases.filter(c => c.status === 'in_progress').length}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <span className="text-2xl">✅</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Resolved</p>
              <p className="text-2xl font-bold text-gray-900">
                {cases.filter(c => c.status === 'completed').length}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <span className="text-2xl">💬</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Followups</p>
              <p className="text-2xl font-bold text-gray-900">
                {cases.reduce((total, c) => total + (c.followups?.length || 0), 0)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Cases Table */}
      {cases.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <div className="text-6xl text-gray-300 mb-4">📋</div>
          <h3 className="text-xl font-semibold text-gray-600 mb-2">No Cases Yet</h3>
          <p className="text-gray-500 mb-6">
            Get started by uploading a PDF document to create your first case
          </p>
          <button
            onClick={handleOpenUploadModal}
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Start Your First Workflow
          </button>
        </div>
      ) : (
        <CasesTable cases={cases} onCaseUpdate={loadCases} />
      )}

      {/* Upload Modal */}
      <UploadModal
        isOpen={showUploadModal}
        onClose={handleCloseUploadModal}
        onWorkflowComplete={handleWorkflowComplete}
      />
    </div>
  );
};

export default CasesPage;
