import React from "react";

const ProgressBar = ({ currentStep, totalSteps }) => {
  return (
    <div className="mb-6">
      <div className="flex justify-between mb-2">
        {Array.from({ length: totalSteps }, (_, i) => (
          <div
            key={i}
            className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
              i + 1 <= currentStep 
                ? "bg-blue-500 text-white" 
                : "bg-gray-200 text-gray-600"
            }`}
          >
            {i + 1}
          </div>
        ))}
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className="bg-blue-500 h-2 rounded-full transition-all duration-300"
          style={{ width: `${(currentStep / totalSteps) * 100}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
