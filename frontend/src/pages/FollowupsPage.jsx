import React, { useState, useEffect } from "react";
import { getFollowups, updateFollowup, deleteFollowup } from "../services/api";

export default function FollowupsPage() {
  const [followups, setFollowups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({});

  useEffect(() => {
    loadFollowups();
  }, []);

  const loadFollowups = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getFollowups();
      setFollowups(data);
    } catch (err) {
      console.error("Failed to load followups:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (followup) => {
    setEditingId(followup.id);
    setEditForm({
      suggestion_text: followup.suggestion_text,
      assigned_to: followup.assigned_to
    });
  };

  const handleSave = async (id) => {
    try {
      await updateFollowup(id, editForm);
      setEditingId(null);
      setEditForm({});
      await loadFollowups();
    } catch (err) {
      console.error("Failed to update followup:", err);
      setError(err.message);
    }
  };

  const handleCancel = () => {
    setEditingId(null);
    setEditForm({});
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this followup?")) {
      try {
        await deleteFollowup(id);
        await loadFollowups();
      } catch (err) {
        console.error("Failed to delete followup:", err);
        setError(err.message);
      }
    }
  };

  // Helper function to get room information
  const getRoomInfo = (followup) => {
    // First try to get room from the followup itself
    if (followup.room) {
      return followup.room;
    }
    
    // Then try to get room from the associated case
    if (followup.cases && followup.cases.room) {
      return followup.cases.room;
    }
    
    // Finally, show case ID if no room is available
    if (followup.case_id) {
      return `Case ID: ${followup.case_id}`;
    }
    
    return 'N/A';
  };

  // Helper function to get case title
  const getCaseTitle = (followup) => {
    if (followup.cases && followup.cases.title) {
      return followup.cases.title;
    }
    return 'No title available';
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">Loading followups...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Followups Management</h1>
          <p className="text-gray-600 mt-1">Manage and track followup tasks</p>
        </div>
        <button
          onClick={loadFollowups}
          className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-medium transition-colors"
        >
          <svg className="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
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

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Room/Case ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Case Title
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Suggestion
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Assigned To
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {followups.map((followup) => (
              <tr key={followup.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {getRoomInfo(followup)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {getCaseTitle(followup)}
                </td>
                <td className="px-6 py-4 text-sm text-gray-900">
                  {editingId === followup.id ? (
                    <input
                      type="text"
                      value={editForm.suggestion_text}
                      onChange={(e) => setEditForm({...editForm, suggestion_text: e.target.value})}
                      className="w-full border border-gray-300 rounded px-2 py-1"
                    />
                  ) : (
                    followup.suggestion_text
                  )}
                </td>

                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {editingId === followup.id ? (
                    <input
                      type="text"
                      value={editForm.assigned_to || ''}
                      onChange={(e) => setEditForm({...editForm, assigned_to: e.target.value})}
                      className="w-full border border-gray-300 rounded px-2 py-1"
                      placeholder="User ID"
                    />
                  ) : (
                    followup.assigned_to || 'Unassigned'
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  {editingId === followup.id ? (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleSave(followup.id)}
                        className="text-green-600 hover:text-green-900"
                      >
                        Save
                      </button>
                      <button
                        onClick={handleCancel}
                        className="text-gray-600 hover:text-gray-900"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEdit(followup)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(followup.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {followups.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <p>No followups found. Upload a PDF to create some!</p>
          </div>
        )}
      </div>
    </div>
  );
}
