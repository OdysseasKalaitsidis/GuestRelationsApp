import React, { useState } from "react";
import {
  uploadPDF,
  generateAI,
  createMultipleCases,
  createFollowup,
} from "../services/api";

const UploadModal = ({ isOpen, onClose, onWorkflowComplete }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfCases, setPdfCases] = useState([]);       // Step 1: PDF data
  const [aiFeedback, setAiFeedback] = useState([]);   // Step 2: AI suggestions
  const [editedCases, setEditedCases] = useState([]); // Step 3: Editable cases
  const [assignedUsers, setAssignedUsers] = useState({});
  const [error, setError] = useState(null);

  const availableUsers = [
    { id: 1, name: "John Smith", role: "Manager" },
    { id: 2, name: "Sarah Johnson", role: "Supervisor" },
    { id: 3, name: "Mike Davis", role: "Staff" },
    { id: 4, name: "Lisa Wilson", role: "Coordinator" },
  ];

  const totalSteps = 4;

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

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Admin Workflow Walkthrough</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700 text-xl">×</button>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between mb-2">
            {Array.from({ length: totalSteps }, (_, i) => (
              <div
                key={i}
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                  i + 1 <= currentStep ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-600"
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
            ></div>
          </div>
        </div>

        {/* Step Title & Description */}
        <div className="mb-6 text-center">
          <h3 className="text-xl font-semibold text-gray-800 mb-2">{getStepTitle()}</h3>
          <p className="text-gray-600">{getStepDescription()}</p>
        </div>

        {/* Step Content */}
        <div className="mb-6">
          {/* Step 1: Upload PDF */}
          {currentStep === 1 && (
            <div className="text-center">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 mb-4">
                <input type="file" accept=".pdf" onChange={handleFileChange} className="hidden" id="pdf-upload" />
                <label htmlFor="pdf-upload" className="cursor-pointer block">
                  <div className="text-6xl text-gray-400 mb-4">📄</div>
                  <p className="text-lg text-gray-600 mb-2">Click to select PDF or drag and drop</p>
                  <p className="text-sm text-gray-500">{pdfFile ? `Selected: ${pdfFile.name}` : 'No file selected'}</p>
                </label>
              </div>
              {error && <p className="text-red-500 mb-4">{error}</p>}
              <button
                onClick={handleUpload}
                disabled={!pdfFile || isLoading}
                className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                {isLoading ? "Processing..." : "Upload PDF"}
              </button>
            </div>
          )}

          {/* Step 2: Review PDF Cases */}
          {currentStep === 2 && (
            <div className="space-y-4">
              {pdfCases.map((c, i) => (
                <div key={i} className="border rounded-lg p-4 bg-gray-50 flex justify-between items-center">
                  <div>
                    <div><strong>Title:</strong> {c.title}</div>
                    <div><strong>Room:</strong> {c.room}</div>
                    <div><strong>Type:</strong> {c.type}</div>
                  </div>
                  <button
                    className="text-red-500 hover:underline"
                    onClick={() => setPdfCases(prev => prev.filter((_, idx) => idx !== i))}
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}

          {/* Step 3: Edit Cases & Assign Users */}
          {currentStep === 3 && (
            <div className="space-y-6">
              {aiFeedback.map((c, i) => (
                <div key={i} className="border rounded-lg p-4 bg-white">
                  <h5 className="font-semibold mb-2">{c.title || 'Untitled Case'}</h5>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <input
                      type="text"
                      value={c.room || ''}
                      onChange={(e) => handleCaseEdit(i, "room", e.target.value)}
                      className="w-full px-3 py-2 border rounded-md"
                      placeholder="Room"
                    />
                    <select
                      value={c.type || ''}
                      onChange={(e) => handleCaseEdit(i, "type", e.target.value)}
                      className="w-full px-3 py-2 border rounded-md"
                    >
                      <option value="">Select Type</option>
                      <option value="maintenance">Maintenance</option>
                      <option value="service">Service</option>
                      <option value="complaint">Complaint</option>
                      <option value="request">Request</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                  <textarea
                    value={c.feedback}
                    onChange={(e) => handleFeedbackEdit(i, e.target.value)}
                    rows={3}
                    className="w-full px-3 py-2 border rounded-md"
                    placeholder="Feedback text"
                  />
                  <select
                    value={assignedUsers[i] || ''}
                    onChange={(e) => handleUserAssignment(i, e.target.value)}
                    className="w-full px-3 py-2 border rounded-md mt-2"
                  >
                    <option value="">Assign User</option>
                    {availableUsers.map(u => (
                      <option key={u.id} value={u.id}>{u.name} ({u.role})</option>
                    ))}
                  </select>
                </div>
              ))}
            </div>
          )}

          {/* Step 4: Confirm & Complete */}
          {currentStep === 4 && (
            <div className="space-y-4">
              {aiFeedback.map((c, i) => (
                <div key={i} className="border rounded-lg p-4 bg-gray-50">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div><strong>Title:</strong> {c.title}</div>
                    <div><strong>Assigned To:</strong> {assignedUsers[i] ? availableUsers.find(u => u.id == assignedUsers[i])?.name : "Unassigned"}</div>
                    <div><strong>Room:</strong> {c.room}</div>
                    <div><strong>Type:</strong> {c.type}</div>
                  </div>
                  <div className="mt-2"><strong>Feedback:</strong> {c.feedback}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Navigation Buttons */}
        <div className="flex justify-between">
          <button
            onClick={prevStep}
            disabled={currentStep === 1}
            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <div className="flex space-x-2">
            {currentStep < totalSteps ? (
              <button
                onClick={nextStep}
                disabled={(currentStep === 1 && pdfCases.length === 0) || isLoading}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                {isLoading ? "Processing..." : "Next"}
              </button>
            ) : (
              <button
                onClick={handleConfirmAll}
                disabled={isLoading}
                className="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                {isLoading ? "Confirming..." : "Confirm & Complete"}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadModal;
