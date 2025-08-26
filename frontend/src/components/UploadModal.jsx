import React, { useState, useEffect } from "react";
import {
  uploadPDF,
  generateAI,
  createMultipleCases,
  createFollowup,
  fetchUsers,
} from "../services/api";
import UploadStep from "./upload/UploadStep";
import ReviewStep from "./upload/ReviewStep";
import EditStep from "./upload/EditStep";
import ConfirmStep from "./upload/ConfirmStep";
import ProgressBar from "./upload/ProgressBar";
import StepHeader from "./upload/StepHeader";
import Navigation from "./upload/Navigation";

const UploadModal = ({ isOpen, onClose, onWorkflowComplete }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfCases, setPdfCases] = useState([]);       // Step 1: PDF data
  const [aiFeedback, setAiFeedback] = useState([]);   // Step 2: AI suggestions
  const [editedCases, setEditedCases] = useState([]); // Step 3: Editable cases
  const [assignedUsers, setAssignedUsers] = useState({});
  const [error, setError] = useState(null);
  const [availableUsers, setAvailableUsers] = useState([]);

  const totalSteps = 4;

  // Fetch users when modal opens
  useEffect(() => {
    if (isOpen) {
      const loadUsers = async () => {
        try {
          const users = await fetchUsers();
          // Transform users to match the expected format
          const transformedUsers = users.map(user => ({
            id: user.id,
            name: user.name,
            role: user.is_admin ? "Admin" : "User"
          }));
          setAvailableUsers(transformedUsers);
        } catch (err) {
          console.error("Failed to fetch users:", err);
          setError("Failed to load users. Please refresh and try again.");
        }
      };
      loadUsers();
    }
  }, [isOpen]);

  // ---------- Step 1: Upload PDF ----------
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/pdf") {
      setPdfFile(file);
      setError(null);
    } else {
      setError("Please select a valid PDF file");
    }
  };

  const handleUpload = async () => {
    if (!pdfFile) {
      setError("Please select a PDF file first");
      return;
    }
    setIsLoading(true);
    setError(null);

    try {
      const extracted = await uploadPDF(pdfFile);
      if (!extracted.cases || extracted.cases.length === 0) {
        setError("No cases found in PDF. Check your document.");
        setIsLoading(false);
        return;
      }

      setPdfCases(extracted.cases);
      setCurrentStep(2);
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to process PDF");
    } finally {
      setIsLoading(false);
    }
  };

  // ---------- Step 2: Generate AI Feedback ----------
  const handleGenerateAI = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const suggestions = await generateAI(pdfCases);
      const feedbackCases = pdfCases.map((c, i) => ({
        ...c,
        feedback: suggestions[i]?.suggestion_text || "No feedback generated",
      }));
      setAiFeedback(feedbackCases);
      setCurrentStep(3);
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to generate AI feedback");
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedbackEdit = (index, newFeedback) => {
    const updated = [...aiFeedback];
    updated[index].feedback = newFeedback;
    setAiFeedback(updated);
  };

  // ---------- Step 3: Edit Cases & Assign Users ----------
  const handleCaseEdit = (index, field, value) => {
    const updated = [...aiFeedback];
    updated[index][field] = value;
    setAiFeedback(updated);
  };

  const handleUserAssignment = (index, userId) => {
    setAssignedUsers((prev) => ({ ...prev, [index]: userId }));
  };

  // ---------- Step 4: Confirm & Create ----------
  const handleConfirmAll = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const finalCases = aiFeedback.map((c, i) => ({
        ...c,
        assignedTo: assignedUsers[i] || null,
      }));

      const createdCases = await createMultipleCases(finalCases);

      for (let i = 0; i < createdCases.length; i++) {
        await createFollowup({
          case_id: createdCases[i].id,
          suggestion_text: finalCases[i].feedback,
          status: "pending",
        });
      }

      onWorkflowComplete();
      onClose();
      setCurrentStep(1);
      setPdfFile(null);
      setPdfCases([]);
      setAiFeedback([]);
      setEditedCases([]);
      setAssignedUsers({});
    } catch (err) {
      console.error(err);
      setError("Failed to confirm changes. Try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const nextStep = () => {
    if (currentStep === 2) handleGenerateAI();
    else if (currentStep < totalSteps) setCurrentStep(currentStep + 1);
  };

  const prevStep = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1: return pdfCases.length > 0;
      case 2: return true;
      case 3: return true;
      case 4: return true;
      default: return false;
    }
  };

  if (!isOpen) return null;

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <UploadStep
            pdfFile={pdfFile}
            onFileChange={handleFileChange}
            onUpload={handleUpload}
            isLoading={isLoading}
            error={error}
          />
        );
      case 2:
        return (
          <ReviewStep
            pdfCases={pdfCases}
            onRemoveCase={(index) => setPdfCases(prev => prev.filter((_, idx) => idx !== index))}
          />
        );
      case 3:
        return (
          <EditStep
            aiFeedback={aiFeedback}
            assignedUsers={assignedUsers}
            availableUsers={availableUsers}
            onCaseEdit={handleCaseEdit}
            onFeedbackEdit={handleFeedbackEdit}
            onUserAssignment={handleUserAssignment}
          />
        );
      case 4:
        return (
          <ConfirmStep
            aiFeedback={aiFeedback}
            assignedUsers={assignedUsers}
            availableUsers={availableUsers}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Admin Workflow Walkthrough</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700 text-xl">×</button>
        </div>

        {/* Progress Bar */}
        <ProgressBar currentStep={currentStep} totalSteps={totalSteps} />

        {/* Step Title & Description */}
        <StepHeader currentStep={currentStep} />

        {/* Step Content */}
        <div className="mb-6">
          {renderStepContent()}
        </div>

        {/* Navigation */}
        <Navigation
          currentStep={currentStep}
          totalSteps={totalSteps}
          onPrevious={prevStep}
          onNext={nextStep}
          onConfirm={handleConfirmAll}
          isLoading={isLoading}
          canProceed={canProceed()}
        />
      </div>
    </div>
  );
};

export default UploadModal;
