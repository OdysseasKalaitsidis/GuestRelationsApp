// src/pages/CasesPage.jsx
import React, { useState, useEffect } from "react";
import CasesTable from "../components/CasesTable";

export default function CasesPage() {
  const [cases, setCases] = useState([]);

  useEffect(() => {
    const savedCases = localStorage.getItem("cases");
    if (savedCases) {
      setCases(JSON.parse(savedCases));
    }
  }, []);

  const generateFollowups = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/ai/feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ cases }),
      });
      const data = await res.json();
      // Update cases with suggested_feedback
      setCases(data.results);
      localStorage.setItem("cases", JSON.stringify(data.results));
    } catch (err) {
      console.error("AI feedback failed:", err);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Cases</h1>
      <button
        onClick={generateFollowups}
        className="mb-4 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
      >
        Generate AI Follow-ups
      </button>
      <CasesTable cases={cases} />
    </div>
  );
}
