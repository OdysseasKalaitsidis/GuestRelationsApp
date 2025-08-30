import React from "react";

const ConfirmStep = ({ aiFeedback, assignedUsers, availableUsers }) => {
  return (
    <div className="space-y-4">
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
