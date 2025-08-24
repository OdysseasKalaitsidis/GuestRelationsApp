const BASE_URL = "http://localhost:8000"; // FastAPI backend

// PDF Processing
export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/pdf/upload`, {
    method: "POST",
    body: formData,
  });
  
  if (!res.ok) {
    throw new Error(`PDF upload failed: ${res.statusText}`);
  }
  
  return res.json();
};

// AI Feedback Generation
export const generateAI = async (cases) => {
  const res = await fetch(`${BASE_URL}/ai/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cases }),
  });
  
  if (!res.ok) {
    throw new Error(`AI feedback generation failed: ${res.statusText}`);
  }
  
  return res.json();
};

// Complete Workflow (PDF → AI → Cases → Followups)
export const completeWorkflow = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/workflow/complete`, {
    method: "POST",
    body: formData,
  });
  
  if (!res.ok) {
    throw new Error(`Workflow failed: ${res.statusText}`);
  }
  
  return res.json();
};

// Case Management
export const createCase = async (caseData) => {
  const res = await fetch(`${BASE_URL}/cases/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(caseData),
  });
  
  if (!res.ok) {
    throw new Error(`Case creation failed: ${res.statusText}`);
  }
  
  return res.json();
};

export const createMultipleCases = async (cases) => {
  const res = await fetch(`${BASE_URL}/cases/bulk`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cases),
  });
  
  if (!res.ok) {
    throw new Error(`Bulk case creation failed: ${res.statusText}`);
  }
  
  return res.json();
};

export const fetchCases = async () => {
  const res = await fetch(`${BASE_URL}/cases/`);
  
  if (!res.ok) {
    throw new Error(`Failed to fetch cases: ${res.statusText}`);
  }
  
  return res.json();
};

export const fetchCasesWithFollowups = async () => {
  const res = await fetch(`${BASE_URL}/cases/with-followups`);
  
  if (!res.ok) {
    throw new Error(`Failed to fetch cases with followups: ${res.statusText}`);
  }
  
  return res.json();
};

export const fetchCaseById = async (id) => {
  const res = await fetch(`${BASE_URL}/cases/${id}`);
  
  if (!res.ok) {
    throw new Error(`Failed to fetch case: ${res.statusText}`);
  }
  
  return res.json();
};

// Followup Management
export const createFollowup = async (followupData) => {
  const res = await fetch(`${BASE_URL}/followups/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(followupData),
  });
  
  if (!res.ok) {
    throw new Error(`Followup creation failed: ${res.statusText}`);
  }
  
  return res.json();
};

export const updateFollowup = async (id, followupData) => {
  const res = await fetch(`${BASE_URL}/followups/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(followupData),
  });
  
  if (!res.ok) {
    throw new Error(`Followup update failed: ${res.statusText}`);
  }
  
  return res.json();
};

export const getFollowups = async () => {
  const res = await fetch(`${BASE_URL}/followups/`);
  
  if (!res.ok) {
    throw new Error(`Failed to fetch followups: ${res.statusText}`);
  }
  
  return res.json();
};

export const getFollowupById = async (id) => {
  const res = await fetch(`${BASE_URL}/followups/${id}`);
  
  if (!res.ok) {
    throw new Error(`Failed to fetch followup: ${res.statusText}`);
  }
  
  return res.json();
};

export const deleteFollowup = async (id) => {
  const res = await fetch(`${BASE_URL}/followups/${id}`, {
    method: "DELETE",
  });
  
  if (!res.ok) {
    throw new Error(`Followup deletion failed: ${res.statusText}`);
  }
  
  return res.json();
};

// Legacy function for backward compatibility
export const saveCases = async (cases) => {
  return createMultipleCases(cases);
};
