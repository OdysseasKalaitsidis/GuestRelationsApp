// Environment configuration
const BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? '/api' : (window.location.origin + "/api"));

// Helper function to get auth token
const getAuthToken = () => {
  return localStorage.getItem('authToken');
};

// Helper function to get auth headers
export const getAuthHeaders = () => {
  const token = getAuthToken();
  return token ? { 'Authorization': `Bearer ${token}` } : {};
};

// Helper function to handle API responses
const handleApiResponse = async (response) => {
  if (!response.ok) {
    // Handle 401 Unauthorized specifically
    if (response.status === 401) {
      // Clear stored auth data and redirect to login
      logout();
      window.location.reload();
      throw new Error('Authentication expired. Please login again.');
    }
    
    let errorMessage = `Request failed: ${response.statusText}`;
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch (e) {
      // If response is not JSON, use status text
    }
    throw new Error(errorMessage);
  }
  return response.json();
};

// Document Processing
export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/documents/upload`, {
    method: "POST",
    headers: {
      ...getAuthHeaders(),
    },
    body: formData,
  });
  
  if (!res.ok) {
    throw new Error(`Document upload failed: ${res.statusText}`);
  }
  
  return res.json();
};

// Legacy function for backward compatibility
export const uploadPDF = async (file) => {
  return uploadDocument(file);
};

// Complete Workflow (PDF → AI → Cases → Followups)
export const completeWorkflow = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/documents/workflow`, {
    method: "POST",
    headers: {
      ...getAuthHeaders(),
    },
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
    headers: { 
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
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
    headers: { 
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(cases),
  });
  
  if (!res.ok) {
    throw new Error(`Bulk case creation failed: ${res.statusText}`);
  }
  
  return res.json();
};

export const fetchCases = async () => {
  const res = await fetch(`${BASE_URL}/cases/`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  if (!res.ok) {
    throw new Error(`Failed to fetch cases: ${res.statusText}`);
  }
  
  return res.json();
};

export const fetchCasesWithFollowups = async () => {
  const res = await fetch(`${BASE_URL}/cases/with-followups`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  if (!res.ok) {
    throw new Error(`Failed to fetch cases with followups: ${res.statusText}`);
  }
  
  return res.json();
};

export const fetchCaseById = async (id) => {
  const res = await fetch(`${BASE_URL}/cases/${id}`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  if (!res.ok) {
    throw new Error(`Failed to fetch case: ${res.statusText}`);
  }
  
  return res.json();
};

// Followup Management
export const createFollowup = async (followupData) => {
  const res = await fetch(`${BASE_URL}/followups/`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
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
    headers: { 
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(followupData),
  });
  
  if (!res.ok) {
    throw new Error(`Followup update failed: ${res.statusText}`);
  }
  
  return res.json();
};

export const getFollowups = async () => {
  const res = await fetch(`${BASE_URL}/followups/with-case-info`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  if (!res.ok) {
    throw new Error(`Failed to fetch followups: ${res.statusText}`);
  }
  
  return res.json();
};

export const getFollowupById = async (id) => {
  const res = await fetch(`${BASE_URL}/followups/${id}`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  if (!res.ok) {
    throw new Error(`Failed to fetch followup: ${res.statusText}`);
  }
  
  return res.json();
};

export const deleteFollowup = async (id) => {
  const res = await fetch(`${BASE_URL}/followups/${id}`, {
    method: "DELETE",
    headers: {
      ...getAuthHeaders(),
    },
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

// Authentication
export const login = async (username, password) => {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);

  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    body: formData,
  });
  
  if (!res.ok) {
    throw new Error(`Login failed: ${res.statusText}`);
  }
  
  const data = await res.json();
  
  // Store token in localStorage
  if (data.access_token) {
    localStorage.setItem('authToken', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
  }
  
  return data;
};

export const logout = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('user');
};

export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};

export const isAuthenticated = () => {
  return !!getAuthToken();
};

// User Management
export const fetchUsers = async () => {
  const res = await fetch(`${BASE_URL}/users/`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  return handleApiResponse(res);
};

export const getCurrentUserInfo = async () => {
  const res = await fetch(`${BASE_URL}/auth/me`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  if (!res.ok) {
    throw new Error(`Failed to fetch user info: ${res.statusText}`);
  }
  
  return res.json();
};

// Task Management
export const fetchTasks = async () => {
  const res = await fetch(`${BASE_URL}/tasks/`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  return handleApiResponse(res);
};

export const createTask = async (taskData) => {
  const res = await fetch(`${BASE_URL}/tasks/`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(taskData),
  });
  
  if (!res.ok) {
    throw new Error(`Task creation failed: ${res.statusText}`);
  }
  
  return res.json();
};

export const createDailyTasks = async (taskDate) => {
  const res = await fetch(`${BASE_URL}/tasks/daily?task_date=${taskDate}`, {
    method: "POST",
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  if (!res.ok) {
    throw new Error(`Daily tasks creation failed: ${res.statusText}`);
  }
  
  return res.json();
};

export const updateTask = async (taskId, taskData) => {
  const res = await fetch(`${BASE_URL}/tasks/${taskId}`, {
    method: "PUT",
    headers: { 
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(taskData),
  });
  
  if (!res.ok) {
    throw new Error(`Task update failed: ${res.statusText}`);
  }
  
  return res.json();
};

export const deleteTask = async (taskId) => {
  const res = await fetch(`${BASE_URL}/tasks/${taskId}`, {
    method: "DELETE",
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  if (!res.ok) {
    throw new Error(`Task deletion failed: ${res.statusText}`);
  }
  
  return res.json();
};

export const getUserTasks = async (userId) => {
  const res = await fetch(`${BASE_URL}/tasks/user/${userId}`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  if (!res.ok) {
    throw new Error(`Failed to fetch user tasks: ${res.statusText}`);
  }
  
  return res.json();
};

// Daily Reset Functions
export const resetDailyCases = async () => {
  const res = await fetch(`${BASE_URL}/cases/reset-daily`, {
    method: "POST",
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  if (!res.ok) {
    throw new Error(`Daily reset failed: ${res.statusText}`);
  }
  
  return res.json();
};



// Case Management
export const updateCaseStatus = async (caseId, status) => {
  const res = await fetch(`${BASE_URL}/cases/${caseId}`, {
    method: "PUT",
    headers: { 
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ status }),
  });
  
  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Failed to update case status: ${res.statusText} - ${errorText}`);
  }
  
  return res.json();
};

// Training Documents
export const getTrainingDocuments = async () => {
  const res = await fetch(`${BASE_URL}/training/documents`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  
  if (!res.ok) {
    throw new Error(`Failed to fetch training documents: ${res.statusText}`);
  }
  
  return res.json();
};

// Email AI Assistant
export const chatWithEmailAssistant = async (emailContent) => {
  const res = await fetch(`${BASE_URL}/chat/email-assistant`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ email_content: emailContent }),
  });
  
  if (!res.ok) {
    throw new Error(`Failed to get AI response: ${res.statusText}`);
  }
  
  return res.json();
};
