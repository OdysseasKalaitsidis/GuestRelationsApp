import React, { useState } from "react";
import { updateCaseStatus } from "../services/api";
import CaseDetailsModal from "./CaseDetailsModal";

export default function CasesTable({ cases, onCaseUpdate }) {
  const [updatingStatus, setUpdatingStatus] = useState(new Set());
  const [detailsModal, setDetailsModal] = useState({
    isOpen: false,
    caseData: null,
    detailType: null
  });

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'in_progress': return 'bg-secondary bg-opacity-20 text-secondary';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      default: return 'bg-third bg-opacity-20 text-third';
    }
  };

  const getImportanceColor = (importance) => {
    switch (importance?.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-third bg-opacity-20 text-third';
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

  const openDetailsModal = (caseData, detailType) => {
    setDetailsModal({
      isOpen: true,
      caseData,
      detailType
    });
  };

  const closeDetailsModal = () => {
    setDetailsModal({
      isOpen: false,
      caseData: null,
      detailType: null
    });
  };

  if (!cases || cases.length === 0) {
    return (
      <div className="text-center py-8 text-third">
        <p>No cases found. Upload a PDF to get started!</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <div className="min-w-full">
        {/* Mobile/Tablet View */}
        <div className="block xl:hidden">
          {cases.map((caseItem) => (
            <div key={caseItem.id} className="bg-white border border-third border-opacity-20 rounded-lg mb-4 p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <span className="text-sm font-medium text-main">Room {caseItem.room || 'N/A'}</span>
                </div>
                <div className="flex items-center">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(caseItem.status)}`}>
                    {caseItem.status || 'pending'}
                  </span>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-3 mb-3 text-sm">
                <div>
                  <span className="text-third">Type:</span>
                  <p className="text-main">{caseItem.type || 'N/A'}</p>
                </div>
                <div>
                  <span className="text-third">Importance:</span>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getImportanceColor(caseItem.importance)}`}>
                    {caseItem.importance || 'N/A'}
                  </span>
                </div>
                <div>
                  <span className="text-third">Assignee:</span>
                  <p className="text-main">
                    {caseItem.assigned_user_name || caseItem.users?.name || (caseItem.owner_id ? `User ${caseItem.owner_id}` : 'Unassigned')}
                  </p>
                </div>
              </div>

              <div className="space-y-2">
                <div>
                  <span className="text-third text-sm">Description:</span>
                  <button
                    onClick={() => openDetailsModal(caseItem, 'description')}
                    className="block w-full text-left text-main text-sm hover:text-secondary transition-colors truncate"
                    title="Click to view full description"
                  >
                    {caseItem.case_description || caseItem.action || 'N/A'}
                  </button>
                </div>
                <div>
                  <span className="text-third text-sm">Action:</span>
                  <button
                    onClick={() => openDetailsModal(caseItem, 'action')}
                    className="block w-full text-left text-main text-sm hover:text-secondary transition-colors truncate"
                    title="Click to view full action"
                  >
                    {caseItem.action || 'N/A'}
                  </button>
                </div>
              </div>

              <div className="mt-3 flex justify-end">
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
              </div>
            </div>
          ))}
        </div>

        {/* Desktop View */}
        <table className="hidden xl:table w-full border border-third border-opacity-20 rounded-lg overflow-hidden shadow-sm">
        <thead className="bg-third bg-opacity-10">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-third uppercase tracking-wider border-b border-third border-opacity-20">
              Room
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-third uppercase tracking-wider border-b border-third border-opacity-20">
              Assignee
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-third uppercase tracking-wider border-b border-third border-opacity-20">
              Importance
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-third uppercase tracking-wider border-b border-third border-opacity-20">
              Type
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-third uppercase tracking-wider border-b border-third border-opacity-20">
              Description
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-third uppercase tracking-wider border-b border-third border-opacity-20">
              Action
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-third uppercase tracking-wider border-b border-third border-opacity-20">
              Status
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-third divide-opacity-20">
          {cases.map((caseItem) => (
            <tr key={caseItem.id} className="hover:bg-third hover:bg-opacity-5">
              <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-main">
                {caseItem.room || 'N/A'}
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-main">
                {caseItem.assigned_user_name || caseItem.users?.name || (caseItem.owner_id ? `User ${caseItem.owner_id}` : 'Unassigned')}
              </td>
              <td className="px-4 py-3 whitespace-nowrap">
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getImportanceColor(caseItem.importance)}`}>
                  {caseItem.importance || 'N/A'}
                </span>
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-main">
                {caseItem.type || 'N/A'}
              </td>
              <td className="px-4 py-3 text-sm text-main max-w-xs">
                <button
                  onClick={() => openDetailsModal(caseItem, 'description')}
                  className="text-left w-full hover:text-secondary transition-colors truncate block"
                  title="Click to view full description"
                >
                  {caseItem.case_description || caseItem.action || 'N/A'}
                </button>
              </td>
              <td className="px-4 py-3 text-sm text-main max-w-xs">
                <button
                  onClick={() => openDetailsModal(caseItem, 'action')}
                  className="text-left w-full hover:text-secondary transition-colors truncate block"
                  title="Click to view full action"
                >
                  {caseItem.action || 'N/A'}
                </button>
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
            </tr>
          ))}
        </tbody>
      </table>
    </div>

    {/* Details Modal */}
    <CaseDetailsModal
      isOpen={detailsModal.isOpen}
      onClose={closeDetailsModal}
      caseData={detailsModal.caseData}
      detailType={detailsModal.detailType}
    />
  </div>
);
}
