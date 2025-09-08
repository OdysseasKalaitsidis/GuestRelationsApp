import React from "react";

const EditStep = ({ 
  aiFeedback, 
  assignedUsers, 
  availableUsers, 
  onFeedbackEdit, 
  onUserAssignment 
}) => {
  return (
    <div className="space-y-6">
      {aiFeedback.map((caseItem, index) => (
        <div key={index} className="border rounded-lg p-6 bg-white shadow-sm">
          {/* Case Header */}
          <div className="flex justify-between items-start mb-6">
            <h5 className="font-semibold text-xl text-gray-800">{caseItem.title || 'Untitled Case'}</h5>
            <div className="flex items-center space-x-2">
              <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-600 rounded">
                Case #{index + 1}
              </span>
            </div>
          </div>
          
          {/* Read-only Case Details Grid */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-gray-50 p-3 rounded-lg">
              <label className="block text-sm font-medium text-gray-600 mb-1">Room</label>
              <div className="text-gray-800 font-medium">{caseItem.room || 'N/A'}</div>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-lg">
              <label className="block text-sm font-medium text-gray-600 mb-1">Status</label>
              <div className="text-gray-800 font-medium">{caseItem.status || 'N/A'}</div>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-lg">
              <label className="block text-sm font-medium text-gray-600 mb-1">Type</label>
              <div className="text-gray-800 font-medium">{caseItem.type || 'N/A'}</div>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-lg">
              <label className="block text-sm font-medium text-gray-600 mb-1">Importance</label>
              <div className="text-gray-800 font-medium">{caseItem.importance || 'N/A'}</div>
            </div>
          </div>
          
          {/* Case Description - Enhanced Read-only Display */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📋 Case Description
            </label>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                {caseItem.case_description || 'No description available'}
              </div>
            </div>
          </div>
          
          {/* Action Required - Enhanced Read-only Display */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              ⚡ Action Required
            </label>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                {caseItem.action || 'No action specified'}
              </div>
            </div>
          </div>
          
          {/* AI Feedback - Editable */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🤖 AI Feedback <span className="text-sm text-gray-500 font-normal">(Editable)</span>
            </label>
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <textarea
                value={caseItem.feedback}
                onChange={(e) => onFeedbackEdit(index, e.target.value)}
                rows={4}
                className="w-full px-3 py-2 border border-yellow-300 rounded-md bg-white text-gray-800 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                placeholder="Edit the AI-generated feedback here..."
              />
            </div>
          </div>
          
          {/* User Assignment */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              👤 Assign User
            </label>
            <select
              value={assignedUsers[index] || ''}
              onChange={(e) => onUserAssignment(index, e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select a user to assign this case</option>
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
