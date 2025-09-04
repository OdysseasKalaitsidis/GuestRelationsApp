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
                ? "bg-secondary text-white" 
                : "bg-third bg-opacity-20 text-third"
            }`}
          >
            {i + 1}
          </div>
        ))}
      </div>
      <div className="w-full bg-third bg-opacity-20 rounded-full h-2">
        <div
          className="bg-secondary h-2 rounded-full transition-all duration-300"
          style={{ width: `${(currentStep / totalSteps) * 100}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
