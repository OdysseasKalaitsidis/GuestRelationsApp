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
          <h5 className="font-semibold mb-4 text-lg">{caseItem.title || 'Untitled Case'}</h5>
          
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Room</label>
              <input
                type="text"
                value={caseItem.room || ''}
                onChange={(e) => onCaseEdit(index, "room", e.target.value)}
                className="w-full px-3 py-2 border rounded-md"
                placeholder="Room"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select
                value={caseItem.status || ''}
                onChange={(e) => onCaseEdit(index, "status", e.target.value)}
                className="w-full px-3 py-2 border rounded-md"
              >
                <option value="">Select Status</option>
                <option value="OPEN">OPEN</option>
                <option value="CLOSED">CLOSED</option>
                <option value="PENDING">PENDING</option>
                <option value="RESOLVED">RESOLVED</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select
                value={caseItem.type || ''}
                onChange={(e) => onCaseEdit(index, "type", e.target.value)}
                className="w-full px-3 py-2 border rounded-md"
              >
                <option value="">Select Type</option>
                <option value="NEGATIVE">NEGATIVE</option>
                <option value="POSITIVE">POSITIVE</option>
                <option value="NEUTRAL">NEUTRAL</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Importance</label>
              <select
                value={caseItem.importance || ''}
                onChange={(e) => onCaseEdit(index, "importance", e.target.value)}
                className="w-full px-3 py-2 border rounded-md"
              >
                <option value="">Select Importance</option>
                <option value="LOW">LOW</option>
                <option value="MEDIUM">MEDIUM</option>
                <option value="HIGH">HIGH</option>
              </select>
            </div>
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Guest</label>
            <input
              type="text"
              value={caseItem.guest || ''}
              onChange={(e) => onCaseEdit(index, "guest", e.target.value)}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="Guest Name"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Case Description</label>
            <textarea
              value={caseItem.case_description || ''}
              onChange={(e) => onCaseEdit(index, "case_description", e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="Case description"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Action</label>
            <textarea
              value={caseItem.action || ''}
              onChange={(e) => onCaseEdit(index, "action", e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="Action taken or required"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">AI Feedback</label>
            <textarea
              value={caseItem.feedback}
              onChange={(e) => onFeedbackEdit(index, e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="Feedback text"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Assign User</label>
            <select
              value={assignedUsers[index] || ''}
              onChange={(e) => onUserAssignment(index, e.target.value)}
              className="w-full px-3 py-2 border rounded-md"
            >
              <option value="">Assign User</option>
              {availableUsers.map(user => (
                <option key={user.id} value={user.id}>
                  {user.name} ({user.role})
                </option>
              ))}
            </select>
          </div>
        </div>
      ))}
    </div>
  );
};

export default EditStep;
