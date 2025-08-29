import React from "react";

const ReviewStep = ({ pdfCases, onRemoveCase }) => {
  return (
    <div className="space-y-4">
      {pdfCases.map((caseItem, index) => (
        <div 
          key={index} 
          className="border rounded-lg p-4 bg-gray-50 flex justify-between items-center"
        >
          <div className="flex-1">
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div><strong>Title:</strong> {caseItem.title}</div>
              <div><strong>Room:</strong> {caseItem.room}</div>
              <div><strong>Status:</strong> {caseItem.status}</div>
              <div><strong>Type:</strong> {caseItem.type}</div>
              <div><strong>Importance:</strong> {caseItem.importance}</div>
              <div><strong>Guest:</strong> {caseItem.guest}</div>
              {caseItem.created && <div><strong>Created:</strong> {caseItem.created}</div>}
              {caseItem.source && <div><strong>Source:</strong> {caseItem.source}</div>}
            </div>
            {caseItem.case_description && (
              <div className="mt-2 text-sm text-gray-600">
                <strong>Description:</strong> {caseItem.case_description}
              </div>
            )}
          </div>
          <button
            className="text-red-500 hover:underline ml-4 flex-shrink-0"
            onClick={() => onRemoveCase(index)}
          >
            Remove
          </button>
        </div>
      ))}
    </div>
  );
};

export default ReviewStep;
