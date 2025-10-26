// Next.js page for task submission
import { useState, useEffect } from "react";

console.log("Orchestrator page loaded");

export default function Orchestrator() {
  const [task, setTask] = useState("");
  const [persona, setPersona] = useState("");
  const [personas, setPersonas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    console.log("Fetching personas from API");
    // Fetch personas from API (placeholder)
    fetch("/api/personas")
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched personas:", data);
        setPersonas(data);
      })
      .catch((err) => console.error("Error fetching personas:", err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitting task:", task, "with persona:", persona);
    setLoading(true);
    try {
      const response = await fetch("/api/orchestrate/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task, persona }),
      });
      const data = await response.json();
      console.log("Received response:", data);
      setResult(data);
    } catch (error) {
      console.error("Error submitting task:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Tribunal AI Orchestrator</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="Enter task description"
          required
        />
        <select
          value={persona}
          onChange={(e) => setPersona(e.target.value)}
          required
        >
          <option value="">Select Persona</option>
          {personas.map((p) => (
            <option key={p.name} value={p.name}>
              {p.name}
            </option>
          ))}
        </select>
        <button type="submit" disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>
      {result && (
        <div>
          <p>Job ID: {result.job_id}</p>
          <p>Status URL: {result.status_url}</p>
        </div>
      )}
    </div>
  );
}
