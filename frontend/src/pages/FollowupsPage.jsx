import { useEffect, useState } from "react";

export default function FollowupsPage() {
  const [followups, setFollowups] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchFollowups = async () => {
    setLoading(true);
    const res = await fetch("http://127.0.0.1:8000/followups");
    const data = await res.json();
    setFollowups(data.followups);
    setLoading(false);
  };

  const markDone = async (id) => {
    await fetch(`http://127.0.0.1:8000/followups/${id}/done`, {
      method: "DELETE",
    });
    setFollowups((prev) => prev.filter((f) => f.id !== id));
  };

  useEffect(() => {
    fetchFollowups();
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Pending Follow-ups</h1>
      {loading && <p>Loading...</p>}
      <div className="flex flex-col gap-4">
        {followups.map((f) => (
          <div key={f.id} className="p-4 border rounded bg-white shadow">
            <p>
              <strong>Suggestion:</strong> {f.suggestion_text}
            </p>
            <p>
              <strong>Case ID:</strong> {f.case_id}
            </p>
            <button
              className="mt-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
              onClick={() => markDone(f.id)}
            >
              Mark Done
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
