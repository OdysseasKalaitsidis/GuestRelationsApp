import React from 'react';

const CaseDetailsModal = ({ isOpen, onClose, caseData, detailType }) => {
  if (!isOpen || !caseData) return null;

  const getDetailContent = () => {
    if (detailType === 'description') {
      return caseData.case_description || caseData.action || 'No description available';
    } else if (detailType === 'action') {
      return caseData.action || 'No action available';
    }
    return '';
  };

  const getDetailTitle = () => {
    if (detailType === 'description') {
      return 'Case Description';
    } else if (detailType === 'action') {
      return 'Required Action';
    }
    return 'Case Details';
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-third border-opacity-20">
          <h2 className="text-xl font-semibold text-main">{getDetailTitle()}</h2>
          <button
            onClick={onClose}
            className="text-third hover:text-main transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {/* Case Info */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-main mb-3">Case Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="text-sm font-medium text-third">Room:</span>
                <p className="text-main">{caseData.room || 'N/A'}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-third">Status:</span>
                <p className="text-main">{caseData.status || 'N/A'}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-third">Type:</span>
                <p className="text-main">{caseData.type || 'N/A'}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-third">Importance:</span>
                <p className="text-main">{caseData.importance || 'N/A'}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-third">Assignee:</span>
                <p className="text-main">
                  {caseData.users ? caseData.users.name : (caseData.owner_id ? `User ${caseData.owner_id}` : 'Unassigned')}
                </p>
              </div>
              <div>
                <span className="text-sm font-medium text-third">Title:</span>
                <p className="text-main">{caseData.title || 'N/A'}</p>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-main mb-3">{getDetailTitle()}</h3>
            <div className="bg-third bg-opacity-10 rounded-lg p-4">
              <p className="text-main whitespace-pre-wrap leading-relaxed">
                {getDetailContent()}
              </p>
            </div>
          </div>

          {/* Followups */}
          {caseData.followups && caseData.followups.length > 0 && (
            <div>
              <h3 className="text-lg font-medium text-main mb-3">Followups ({caseData.followups.length})</h3>
              <div className="space-y-3">
                {caseData.followups.map((followup, index) => (
                  <div key={followup.id} className="bg-white border border-third border-opacity-20 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <span className="text-sm font-medium text-third">Followup #{index + 1}</span>
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        followup.status === 'completed' ? 'bg-green-100 text-green-800' :
                        followup.status === 'in_progress' ? 'bg-secondary bg-opacity-20 text-secondary' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {followup.status || 'pending'}
                      </span>
                    </div>
                    <p className="text-main text-sm leading-relaxed">
                      {followup.suggestion_text}
                    </p>
                    {followup.assigned_to && (
                      <p className="text-xs text-third mt-2">
                        Assigned to: {followup.assigned_to}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t border-third border-opacity-20">
          <button
            onClick={onClose}
            className="bg-secondary text-white px-4 py-2 rounded-lg hover:bg-secondary hover:bg-opacity-80 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default CaseDetailsModal;

