import React, { useState, useEffect } from "react";
import {
  uploadPDF,
  createMultipleCases,
  createFollowup,
  fetchUsers,
  uploadDocument,
  completeWorkflow,
  getAuthHeaders,
} from "../services/api";
import UploadStep from "./upload/UploadStep";
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
  const [processingStatus, setProcessingStatus] = useState({ message: '', progress: 0, current: 0, total: 0 });

  const totalSteps = 3;

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

  // ---------- Step 1: Upload Document ----------
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && (file.type === "application/pdf" || file.name.toLowerCase().endsWith('.docx'))) {
      setPdfFile(file);
      setError(null);
    } else {
      setError("Please select a valid PDF or Word document (.pdf or .docx)");
    }
  };

  const handleUpload = async () => {
    if (!pdfFile) {
      setError("Please select a document file first");
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setProcessingStatus({ message: 'Starting upload...', progress: 0, current: 0, total: 0 });

    try {
      // Use streaming workflow endpoint for real-time progress
      const formData = new FormData();
      formData.append("file", pdfFile);
      formData.append("create_cases", "false");
      
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/documents/workflow-stream`, {
        method: "POST",
        headers: {
          ...getAuthHeaders(),
        },
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Workflow failed: ${response.statusText}`);
      }
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let cases = [];
      let suggestions = [];
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              // Update processing status
              setProcessingStatus({
                message: data.message,
                progress: data.progress || 0,
                current: data.current || 0,
                total: data.total || 0
              });
              
              // Handle different steps
              if (data.step === 'parsing') {
                cases = data.cases || [];
                setPdfCases(cases);
              } else if (data.step === 'complete') {
                cases = data.cases || [];
                suggestions = data.suggestions || [];
                
                // Map feedback to cases
                const casesWithFeedback = cases.map((c, i) => ({
                  ...c,
                  feedback: suggestions[i]?.suggestion_text || "No AI feedback generated - please add manual feedback",
                }));
                
                setAiFeedback(casesWithFeedback);
                setCurrentStep(2); // Go to step 2 (previously step 3)
              } else if (data.step === 'error') {
                setError(data.message);
                setIsLoading(false);
                return;
              }
            } catch (e) {
              console.warn('Failed to parse progress data:', e);
            }
          }
        }
      }
      
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to process document");
    } finally {
      setIsLoading(false);
    }
  };


  const handleFeedbackEdit = (index, newFeedback) => {
    const updated = [...aiFeedback];
    updated[index].feedback = newFeedback;
    setAiFeedback(updated);
  };

  // ---------- Step 2: Edit AI Feedback & Assign Users ----------

  const handleUserAssignment = (index, userId) => {
    setAssignedUsers((prev) => ({ ...prev, [index]: userId }));
  };

  // ---------- Step 3: Confirm & Create ----------
  const handleConfirmAll = async () => {
    setIsLoading(true);
    setError(null);
    try {
      let finalCases = aiFeedback.map((c, i) => ({
        room: c.room,
        status: c.status,
        importance: c.importance,
        type: c.type,
        title: c.title,
        action: c.action,
        guest: c.guest,
        created: c.created,
        created_by: c.created_by,
        modified: c.modified,
        modified_by: c.modified_by,
        source: c.source,
        membership: c.membership,
        case_description: c.case_description,
        in_out: c.in_out,
        owner_id: assignedUsers[i] || null,
      }));

      // Automatically anonymize all data for GDPR compliance
      const anonymizedCases = await Promise.all(
        finalCases.map(async (caseData) => {
          const anonymizedCase = { ...caseData };
          
          // Anonymize guest names
          if (anonymizedCase.guest) {
            anonymizedCase.guest = '[CLIENT_NAME]';
          }
          
          // Anonymize created_by and modified_by
          if (anonymizedCase.created_by) {
            anonymizedCase.created_by = '[STAFF_MEMBER]';
          }
          if (anonymizedCase.modified_by) {
            anonymizedCase.modified_by = '[STAFF_MEMBER]';
          }
          
          // Use backend anonymization service for case description
          if (anonymizedCase.case_description) {
            try {
              const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/anonymization/text`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  ...getAuthHeaders(),
                },
                body: JSON.stringify({
                  text: anonymizedCase.case_description,
                  preserve_dates: false, // Don't preserve dates for full GDPR compliance
                  preserve_times: false, // Don't preserve times for full GDPR compliance
                }),
              });
              
              if (response.ok) {
                const result = await response.json();
                anonymizedCase.case_description = result.anonymized_text;
              } else {
                // Fallback to simple replacement if service fails
                anonymizedCase.case_description = anonymizedCase.case_description
                  .replace(/\b[A-Z][a-z]+ [A-Z][a-z]+\b/g, '[CLIENT_NAME]')
                  .replace(/\b[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+\b/g, '[CLIENT_NAME]')
                  .replace(/\b[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+\b/g, '[CLIENT_NAME]');
              }
            } catch (anonError) {
              console.warn("Anonymization service failed, using fallback:", anonError);
              // Fallback to simple replacement
              anonymizedCase.case_description = anonymizedCase.case_description
                .replace(/\b[A-Z][a-z]+ [A-Z][a-z]+\b/g, '[CLIENT_NAME]')
                .replace(/\b[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+\b/g, '[CLIENT_NAME]')
                .replace(/\b[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+\b/g, '[CLIENT_NAME]');
            }
          }
          
          // Anonymize dates and times for full GDPR compliance
          if (anonymizedCase.created) {
            anonymizedCase.created = '[DATE]';
          }
          if (anonymizedCase.modified) {
            anonymizedCase.modified = '[DATE]';
          }
          
          return anonymizedCase;
        })
      );

      const createdCases = await createMultipleCases(anonymizedCases);

      for (let i = 0; i < createdCases.length; i++) {
        await createFollowup({
          case_id: createdCases[i].id,
          suggestion_text: aiFeedback[i].feedback,
          assigned_to: assignedUsers[i] || null,
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
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1: return pdfCases.length > 0;
      case 2: return true;
      case 3: return true;
      default: return false;
    }
  };

  if (!isOpen) return null;

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div>
            <UploadStep
              pdfFile={pdfFile}
              onFileChange={handleFileChange}
              onUpload={handleUpload}
              isLoading={isLoading}
              error={error}
            />
            
          </div>
        );
      case 2:
        return (
          <EditStep
            aiFeedback={aiFeedback}
            assignedUsers={assignedUsers}
            availableUsers={availableUsers}
            onFeedbackEdit={handleFeedbackEdit}
            onUserAssignment={handleUserAssignment}
          />
        );
      case 3:
        return (
          <ConfirmStep
            aiFeedback={aiFeedback}
            assignedUsers={assignedUsers}
            availableUsers={availableUsers}
            anonymizeData={true}
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
          <h2 className="text-2xl font-bold text-main">Admin Workflow Walkthrough</h2>
          <button onClick={onClose} className="text-third hover:text-main text-xl">×</button>
        </div>

        {/* Progress Bar */}
        <ProgressBar currentStep={currentStep} totalSteps={totalSteps} />

        {/* Step Title & Description */}
        <StepHeader currentStep={currentStep} />

        {/* Processing Status */}
        {isLoading && processingStatus.message && (
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="text-blue-800 font-medium">{processingStatus.message}</span>
              <span className="text-blue-600 text-sm">{processingStatus.progress}%</span>
            </div>
            <div className="w-full bg-blue-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                style={{ width: `${processingStatus.progress}%` }}
              ></div>
            </div>
            {processingStatus.current > 0 && processingStatus.total > 0 && (
              <div className="text-blue-600 text-sm mt-1">
                Processing case {processingStatus.current} of {processingStatus.total}
              </div>
            )}
          </div>
        )}

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
