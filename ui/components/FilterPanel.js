// React component for KG filters with advanced psychological/investigative options
import { useState } from "react";

export default function FilterPanel({ filter, setFilter, nodes, edges }) {
  const applyFilters = () => {
    // Apply filters to nodes and edges
    let filteredNodes = nodes;
    let filteredEdges = edges;

    if (filter.nodeType) {
      filteredNodes = filteredNodes.filter(
        (node) => node.type === filter.nodeType
      );
    }

    if (filter.relationship) {
      filteredEdges = filteredEdges.filter(
        (edge) => edge.relationship === filter.relationship
      );
    }

    if (filter.motive) {
      filteredNodes = filteredNodes.filter(
        (node) =>
          node.type === "Motive" &&
          node.name.toLowerCase().includes(filter.motive.toLowerCase())
      );
    }

    if (filter.context) {
      filteredNodes = filteredNodes.filter(
        (node) =>
          node.type === "Context" &&
          node.name.toLowerCase().includes(filter.context.toLowerCase())
      );
    }

    // Update parent state with filtered data
    // Note: In a full implementation, this would trigger a re-render of the Cytoscape graph
    console.log("Applied filters:", {
      filteredNodes: filteredNodes.length,
      filteredEdges: filteredEdges.length,
    });
  };

  const clearFilters = () => {
    setFilter({ nodeType: "", relationship: "", motive: "", context: "" });
  };

  return (
    <div
      style={{
        padding: "15px",
        border: "1px solid #ddd",
        marginBottom: "20px",
        borderRadius: "5px",
        backgroundColor: "#fafafa",
      }}
    >
      <h3 style={{ marginTop: 0 }}>Advanced Filters</h3>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "15px",
          alignItems: "center",
        }}
      >
        <div>
          <label
            style={{
              display: "block",
              marginBottom: "5px",
              fontWeight: "bold",
            }}
          >
            Node Type:
          </label>
          <select
            value={filter.nodeType}
            onChange={(e) => setFilter({ ...filter, nodeType: e.target.value })}
            style={{ padding: "5px", minWidth: "120px" }}
          >
            <option value="">All Node Types</option>
            <option value="Party">Party</option>
            <option value="Contract">Contract</option>
            <option value="Document">Document</option>
            <option value="Statute">Statute</option>
            <option value="Event">Event</option>
            <option value="Location">Location</option>
            <option value="Motive">Motive</option>
            <option value="Context">Context</option>
            <option value="EvidenceCategory">Evidence Category</option>
            <option value="PsychologicalProfile">Psychological Profile</option>
            <option value="CommunicationStyle">Communication Style</option>
            <option value="PredictiveIndicator">Predictive Indicator</option>
          </select>
        </div>

        <div>
          <label
            style={{
              display: "block",
              marginBottom: "5px",
              fontWeight: "bold",
            }}
          >
            Relationship:
          </label>
          <select
            value={filter.relationship}
            onChange={(e) =>
              setFilter({ ...filter, relationship: e.target.value })
            }
            style={{ padding: "5px", minWidth: "120px" }}
          >
            <option value="">All Relationships</option>
            <option value="PART_OF">Part Of</option>
            <option value="CONTRACTED_PARTY">Contracted Party</option>
            <option value="REFERRED_TO_STATUTE">Referred to Statute</option>
            <option value="OCCURRED_AT_LOCATION">Occurred at Location</option>
            <option value="ALLEGED_MISCONDUCT">Alleged Misconduct</option>
            <option value="INFLUENCES">Influences</option>
            <option value="PREDICTS">Predicts</option>
            <option value="COMMUNICATES_VIA">Communicates Via</option>
            <option value="EVIDENCE_OF">Evidence Of</option>
            <option value="PSYCHOLOGICAL_LINK">Psychological Link</option>
            <option value="STRATEGIC_CONNECTION">Strategic Connection</option>
          </select>
        </div>

        <div>
          <label
            style={{
              display: "block",
              marginBottom: "5px",
              fontWeight: "bold",
            }}
          >
            Motive Contains:
          </label>
          <input
            type="text"
            value={filter.motive}
            onChange={(e) => setFilter({ ...filter, motive: e.target.value })}
            placeholder="e.g., financial, power"
            style={{ padding: "5px", minWidth: "120px" }}
          />
        </div>

        <div>
          <label
            style={{
              display: "block",
              marginBottom: "5px",
              fontWeight: "bold",
            }}
          >
            Context Contains:
          </label>
          <input
            type="text"
            value={filter.context}
            onChange={(e) => setFilter({ ...filter, context: e.target.value })}
            placeholder="e.g., risk, urgent"
            style={{ padding: "5px", minWidth: "120px" }}
          />
        </div>

        <div style={{ display: "flex", gap: "10px", alignItems: "flex-end" }}>
          <button
            onClick={applyFilters}
            style={{
              padding: "8px 16px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "3px",
              cursor: "pointer",
            }}
          >
            Apply Filters
          </button>
          <button
            onClick={clearFilters}
            style={{
              padding: "8px 16px",
              backgroundColor: "#6c757d",
              color: "white",
              border: "none",
              borderRadius: "3px",
              cursor: "pointer",
            }}
          >
            Clear Filters
          </button>
        </div>
      </div>
    </div>
  );
}
