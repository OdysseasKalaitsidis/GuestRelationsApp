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

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-secondary mx-auto mb-4"></div>
          <p className="text-third">Loading cases...</p>
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
            className="bg-secondary text-white px-4 py-2 rounded-lg hover:bg-secondary hover:bg-opacity-80"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full px-4 py-8">
      {/* Header */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-8 gap-4">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold text-main mb-2">Daily Guest Relations Case Management</h1>
          <p className="text-third">
            View and manage all guest relations cases
          </p>
        </div>
        <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3 w-full lg:w-auto">
          <button
            onClick={handleOpenUploadModal}
            className="bg-secondary text-white px-4 lg:px-6 py-2 lg:py-3 rounded-lg hover:bg-secondary hover:bg-opacity-80 transition-colors flex items-center justify-center space-x-2"
          >
            <span>📄</span>
            <span>Upload Daily Cases</span>
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-secondary bg-opacity-20 rounded-lg">
              <span className="text-2xl">📋</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-third">Total Cases</p>
              <p className="text-2xl font-bold text-main">{cases.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <span className="text-2xl">⏳</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-third">In Progress</p>
              <p className="text-2xl font-bold text-main">
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
              <p className="text-sm font-medium text-third">Resolved</p>
              <p className="text-2xl font-bold text-main">
                {cases.filter(c => c.status === 'completed').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Cases Table */}
      {cases.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <div className="text-6xl text-third mb-4">📋</div>
          <h3 className="text-xl font-semibold text-third mb-2">No Cases Yet</h3>
          <p className="text-third mb-6">
            Get started by uploading a PDF document to create your first case
          </p>
          <button
            onClick={handleOpenUploadModal}
            className="bg-secondary text-white px-6 py-3 rounded-lg hover:bg-secondary hover:bg-opacity-80 transition-colors"
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
