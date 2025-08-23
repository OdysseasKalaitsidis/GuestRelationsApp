import { useState } from "react";
import { generateAI } from "../services/api";

export default function CasesPage({ initialCases }) {
  const [cases, setCases] = useState(initialCases || []);

  const handleGenerate = async () => {
    const data = await generateAI(cases);
    setCases(data.results);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">All Cases</h1>
      <button
        onClick={handleGenerate}
        className="mb-4 px-4 py-2 bg-green-500 text-white rounded"
      >
        Generate AI Follow-up
      </button>

      <table className="min-w-full border">
        <thead>
          <tr>
            <th className="border px-4 py-2">Room</th>
            <th className="border px-4 py-2">Status</th>
            <th className="border px-4 py-2">Assigned Agent</th>
            <th className="border px-4 py-2">Suggested Follow-up</th>
          </tr>
        </thead>
        <tbody>
          {cases.map((c, i) => (
            <tr key={i}>
              <td className="border px-4 py-2">{c.room}</td>
              <td className="border px-4 py-2">{c.status}</td>
              <td className="border px-4 py-2">
                {c.assigned_to || "Unassigned"}
              </td>
              <td className="border px-4 py-2">
                {c.suggested_feedback || "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
