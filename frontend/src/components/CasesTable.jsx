import React, { useState } from "react";
import { updateCaseStatus } from "../services/api";

export default function CasesTable({ cases, onCaseUpdate }) {
  const [expandedRows, setExpandedRows] = useState(new Set());
  const [updatingStatus, setUpdatingStatus] = useState(new Set());

  const toggleRow = (caseId) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(caseId)) {
      newExpanded.delete(caseId);
    } else {
      newExpanded.add(caseId);
    }
    setExpandedRows(newExpanded);
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getImportanceColor = (importance) => {
    switch (importance?.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleStatusUpdate = async (caseId, newStatus) => {
    try {
      setUpdatingStatus(prev => new Set(prev).add(caseId));
      console.log('Updating case', caseId, 'to status', newStatus);
      const result = await updateCaseStatus(caseId, newStatus);
      console.log('Update result:', result);
      
      // Call the parent component's update function to refresh the cases
      if (onCaseUpdate) {
        onCaseUpdate();
      }
    } catch (error) {
      console.error('Failed to update case status:', error);
      alert(`Failed to update case status: ${error.message}`);
    } finally {
      setUpdatingStatus(prev => {
        const newSet = new Set(prev);
        newSet.delete(caseId);
        return newSet;
      });
    }
  };

  if (!cases || cases.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No cases found. Upload a PDF to get started!</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full border border-gray-200 rounded-lg overflow-hidden shadow-sm">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
              Room
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
              Status
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
              Importance
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
              Type
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
              Title
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
              Action
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
              Followups
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {cases.map((caseItem) => (
            <React.Fragment key={caseItem.id}>
              <tr className="hover:bg-gray-50">
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                  {caseItem.room || 'N/A'}
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <select
                    value={caseItem.status || ''}
                    onChange={(e) => handleStatusUpdate(caseItem.id, e.target.value)}
                    disabled={updatingStatus.has(caseItem.id)}
                    className={`text-xs font-semibold rounded-full border-0 px-2 py-1 ${getStatusColor(caseItem.status)} ${
                      updatingStatus.has(caseItem.id) ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
                    }`}
                  >
                    <option value="pending">Pending</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                    <option value="rejected">Rejected</option>
                  </select>
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getImportanceColor(caseItem.importance)}`}>
                    {caseItem.importance || 'N/A'}
                  </span>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                  {caseItem.type || 'N/A'}
                </td>
                <td className="px-4 py-3 text-sm text-gray-900 max-w-xs truncate">
                  {caseItem.title || 'N/A'}
                </td>
                <td className="px-4 py-3 text-sm text-gray-900 max-w-xs truncate">
                  {caseItem.action || 'N/A'}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {caseItem.followups?.length || 0} followups
                  </span>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                  <button
                    onClick={() => toggleRow(caseItem.id)}
                    className="text-blue-600 hover:text-blue-900 text-sm font-medium"
                  >
                    {expandedRows.has(caseItem.id) ? 'Hide' : 'Show'} Details
                  </button>
                </td>
              </tr>
              
              {/* Expanded row showing followups */}
              {expandedRows.has(caseItem.id) && caseItem.followups && caseItem.followups.length > 0 && (
                <tr>
                  <td colSpan="8" className="px-4 py-3 bg-gray-50">
                    <div className="space-y-3">
                      <h4 className="font-medium text-gray-900">Followups:</h4>
                      <div className="grid gap-3">
                        {caseItem.followups.map((followup) => (
                          <div key={followup.id} className="bg-white p-3 rounded-lg border border-gray-200">
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <p className="text-sm text-gray-900 mb-1">
                                  <span className="font-medium">Suggestion:</span> {followup.suggestion_text}
                                </p>
                                <div className="flex items-center gap-4 text-xs text-gray-500">
                                  <span>
                                    <span className="font-medium">Status:</span> 
                                    <span className={`ml-1 inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(followup.status)}`}>
                                      {followup.status || 'pending'}
                                    </span>
                                  </span>
                                  {followup.assigned_to && (
                                    <span>
                                      <span className="font-medium">Assigned to:</span> {followup.assigned_to}
                                    </span>
                                  )}
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
}
