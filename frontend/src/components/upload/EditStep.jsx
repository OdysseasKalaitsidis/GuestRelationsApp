import React from "react";

const EditStep = ({ 
  aiFeedback, 
  assignedUsers, 
  availableUsers, 
  onCaseEdit, 
  onFeedbackEdit, 
  onUserAssignment 
}) => {
  return (
    <div className="space-y-6">
      {aiFeedback.map((caseItem, index) => (
        <div key={index} className="border rounded-lg p-4 bg-white">
          <h5 className="font-semibold mb-2">{caseItem.title || 'Untitled Case'}</h5>
          
          <div className="mb-4">
            <input
              type="text"
              value={caseItem.room || ''}
              onChange={(e) => onCaseEdit(index, "room", e.target.value)}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="Room"
            />
          </div>
          
          <textarea
            value={caseItem.feedback}
            onChange={(e) => onFeedbackEdit(index, e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border rounded-md"
            placeholder="Feedback text"
          />
          
          <select
            value={assignedUsers[index] || ''}
            onChange={(e) => onUserAssignment(index, e.target.value)}
            className="w-full px-3 py-2 border rounded-md mt-2"
          >
            <option value="">Assign User</option>
            {availableUsers.map(user => (
              <option key={user.id} value={user.id}>
                {user.name} ({user.role})
              </option>
            ))}
          </select>
        </div>
      ))}
    </div>
  );
};

export default EditStep;
