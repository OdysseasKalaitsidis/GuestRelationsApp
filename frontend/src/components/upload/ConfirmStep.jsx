import React from "react";

const ConfirmStep = ({ aiFeedback, assignedUsers, availableUsers, anonymizeData }) => {
  return (
    <div className="space-y-4">
      {anonymizeData && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
          <div className="flex items-center">
            <div className="text-blue-600 mr-2">🔒</div>
            <div>
              <strong className="text-blue-800">GDPR Compliance Enabled</strong>
              <p className="text-blue-700 text-sm mt-1">
                Personal data will be anonymized before saving. Names will be replaced with [CLIENT_NAME] and [STAFF_MEMBER].
              </p>
            </div>
          </div>
        </div>
      )}
      
      {aiFeedback.map((caseItem, index) => (
        <div key={index} className="border rounded-lg p-4 bg-gray-50">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div><strong>Title:</strong> {caseItem.title}</div>
            <div>
              <strong>Assigned To:</strong> {
                assignedUsers[index] 
                  ? availableUsers.find(u => u.id == assignedUsers[index])?.name 
                  : "Unassigned"
              }
            </div>
            <div><strong>Room:</strong> {caseItem.room}</div>
          </div>
          <div className="mt-2">
            <strong>Feedback:</strong> {caseItem.feedback}
          </div>
          {caseItem.action && (
            <div className="mt-2">
              <strong>Action:</strong> {caseItem.action}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default ConfirmStep;
