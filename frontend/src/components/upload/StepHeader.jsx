import React from "react";

const StepHeader = ({ currentStep }) => {
  const getStepTitle = () => {
    switch (currentStep) {
      case 1: return "Step 1: Upload Document";
      case 2: return "Step 2: Auto-Processing";
      case 3: return "Step 3: Edit Cases & Assign Users";
      case 4: return "Step 4: Confirm & Complete";
      default: return "";
    }
  };

  const getStepDescription = () => {
    switch (currentStep) {
      case 1: return "Upload a PDF or Word document. ⚠️ This will clear all existing data before processing.";
      case 2: return "Automatically processing document and generating AI feedback...";
      case 3: return "Edit case details and assign responsible users.";
      case 4: return "Review and confirm all cases and followups.";
      default: return "";
    }
  };

  return (
    <div className="mb-6 text-center">
      <h3 className="text-xl font-semibold text-main mb-2">
        {getStepTitle()}
      </h3>
      <p className="text-third">{getStepDescription()}</p>
    </div>
  );
};

export default StepHeader;
