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
    <div style={{ padding: "20px", maxWidth: "800px", margin: "0 auto" }}>
      <h1>Tribunal AI Orchestrator</h1>
      <p>
        Submit legal analysis tasks to be processed by specialized AI personas
        with access to the knowledge graph.
      </p>

      <form onSubmit={handleSubmit} style={{ marginBottom: "30px" }}>
        <div style={{ marginBottom: "15px" }}>
          <label
            style={{
              display: "block",
              marginBottom: "5px",
              fontWeight: "bold",
            }}
          >
            Task Description:
          </label>
          <textarea
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="Describe the legal analysis task (e.g., 'Analyze contract disputes involving Party A and Party B')"
            required
            style={{
              width: "100%",
              minHeight: "100px",
              padding: "10px",
              border: "1px solid #ccc",
              borderRadius: "4px",
            }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label
            style={{
              display: "block",
              marginBottom: "5px",
              fontWeight: "bold",
            }}
          >
            AI Persona:
          </label>
          <select
            value={persona}
            onChange={(e) => setPersona(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "10px",
              border: "1px solid #ccc",
              borderRadius: "4px",
            }}
          >
            <option value="">Select AI Persona</option>
            {personas.map((p) => (
              <option key={p.name} value={p.name}>
                {p.name} - {p.description}
              </option>
            ))}
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "12px 24px",
            backgroundColor: loading ? "#6c757d" : "#007bff",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: loading ? "not-allowed" : "pointer",
            fontSize: "16px",
          }}
        >
          {loading ? "Submitting Task..." : "Submit Task"}
        </button>
      </form>

      {result && (
        <div
          style={{
            padding: "15px",
            backgroundColor: "#d4edda",
            border: "1px solid #c3e6cb",
            borderRadius: "4px",
            marginBottom: "20px",
          }}
        >
          <h3>Task Submitted Successfully</h3>
          <p>
            <strong>Job ID:</strong> {result.job_id}
          </p>
          <p>
            <strong>Status URL:</strong>{" "}
            <a
              href={result.status_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              {result.status_url}
            </a>
          </p>
          <p>
            You can check the job status at the provided URL. Processing may
            take several minutes depending on task complexity.
          </p>
        </div>
      )}

      {/* Link to KG Studio */}
      <div
        style={{
          marginTop: "40px",
          padding: "20px",
          backgroundColor: "#f8f9fa",
          borderRadius: "8px",
          textAlign: "center",
        }}
      >
        <h3>Explore Knowledge Graph</h3>
        <p>
          View and analyze the underlying knowledge graph that powers our AI
          analysis.
        </p>
        <a
          href="/kg-studio"
          style={{
            display: "inline-block",
            padding: "10px 20px",
            backgroundColor: "#28a745",
            color: "white",
            textDecoration: "none",
            borderRadius: "4px",
            fontWeight: "bold",
          }}
        >
          Open KG Studio
        </a>
      </div>
    </div>
  );
}
