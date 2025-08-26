import React from "react";

const Navigation = ({ 
  currentStep, 
  totalSteps, 
  onPrevious, 
  onNext, 
  onConfirm, 
  isLoading,
  canProceed 
}) => {
  return (
    <div className="flex justify-between">
      <button
        onClick={onPrevious}
        disabled={currentStep === 1}
        className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Previous
      </button>
      
      <div className="flex space-x-2">
        {currentStep < totalSteps ? (
          <button
            onClick={onNext}
            disabled={!canProceed || isLoading}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {isLoading ? "Processing..." : "Next"}
          </button>
        ) : (
          <button
            onClick={onConfirm}
            disabled={isLoading}
            className="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {isLoading ? "Confirming..." : "Confirm & Complete"}
          </button>
        )}
      </div>
    </div>
  );
};

export default Navigation;
