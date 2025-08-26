import React from "react";

const ReviewStep = ({ pdfCases, onRemoveCase }) => {
  return (
    <div className="space-y-4">
      {pdfCases.map((caseItem, index) => (
        <div 
          key={index} 
          className="border rounded-lg p-4 bg-gray-50 flex justify-between items-center"
        >
          <div>
            <div><strong>Title:</strong> {caseItem.title}</div>
            <div><strong>Room:</strong> {caseItem.room}</div>
            <div><strong>Type:</strong> {caseItem.type}</div>
          </div>
          <button
            className="text-red-500 hover:underline"
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
