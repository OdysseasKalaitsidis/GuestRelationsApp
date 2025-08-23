const BASE_URL = "http://localhost:8000"; // FastAPI backend

export async function uploadPDF(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/pdf/upload`, {
    method: "POST",
    body: formData,
  });

  return res.json(); // returns { cases: [...] }
}

export async function generateAI(cases) {
  const res = await fetch(`${BASE_URL}/ai/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cases }),
  });

  return res.json(); // returns { results: [...] }
}

export async function getFollowups() {
  const res = await fetch(`${BASE_URL}/followups/`);
  return res.json();
}

export async function deleteFollowup(id) {
  const res = await fetch(`${BASE_URL}/followups/${id}`, {
    method: "DELETE",
  });
  return res.json();
}
