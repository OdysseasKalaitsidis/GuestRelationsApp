import React from "react";

const StepHeader = ({ currentStep }) => {
  const getStepTitle = () => {
    switch (currentStep) {
      case 1: return "Step 1: Upload Document";
      case 2: return "Step 2: Review & Edit AI Feedback";
      case 3: return "Step 3: Confirm & Complete";
      default: return "";
    }
  };

  const getStepDescription = () => {
    switch (currentStep) {
      case 1: return "Upload a PDF or Word document. ⚠️ This will clear all existing data before processing.";
      case 2: return "Review the AI-generated feedback and edit as needed. Case details are read-only.";
      case 3: return "Review and confirm all cases and followups.";
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
