import React from "react";

const StepHeader = ({ currentStep }) => {
  const getStepTitle = () => {
    switch (currentStep) {
      case 1: return "Step 1: Upload PDF";
      case 2: return "Step 2: Review PDF Cases";
      case 3: return "Step 3: Edit Cases & Assign Users";
      case 4: return "Step 4: Confirm & Complete";
      default: return "";
    }
  };

  const getStepDescription = () => {
    switch (currentStep) {
      case 1: return "Upload a PDF to extract cases.";
      case 2: return "Inspect the extracted cases from the PDF.";
      case 3: return "Edit case details and assign responsible users.";
      case 4: return "Review and confirm all cases and followups.";
      default: return "";
    }
  };

  return (
    <div className="mb-6 text-center">
      <h3 className="text-xl font-semibold text-gray-800 mb-2">
        {getStepTitle()}
      </h3>
      <p className="text-gray-600">{getStepDescription()}</p>
    </div>
  );
};

export default StepHeader;
