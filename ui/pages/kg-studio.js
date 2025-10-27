// Next.js page for KG Studio with Cytoscape visualization
import { useState, useEffect, useRef } from "react";
import cytoscape from "cytoscape";
import coseBilkent from "cytoscape-cose-bilkent";

  useEffect(() => {
    if (cyRef.current && nodes.length > 0) {
      const cy = cytoscape({
        container: cyRef.current,
        elements: [
          ...nodes.map((node) => ({
            data: { id: node.id, label: node.name, type: node.type },
            classes: node.type.toLowerCase()
          })),
          ...edges.map((edge) => ({
            data: {
              source: edge.source,
              target: edge.target,
              label: edge.relationship,
              proof: edge.proof
            },
          })),
        ],
        style: [
          {
            selector: "node",
            style: {
              "background-color": (ele) => {
                const typeColors = {
                  party: "#ff6b6b",
                  contract: "#4ecdc4",
                  document: "#45b7d1",
                  motive: "#f9ca24",
                  context: "#6c5ce7",
                  communicationstyle: "#a29bfe",
                  default: "#666"
                };
                return typeColors[ele.data('type').toLowerCase()] || typeColors.default;
              },
              label: "data(label)",
              "text-valign": "center",
              "text-halign": "center",
              "font-size": "12px",
              width: 40,
              height: 40
            },
          },
          {
            selector: "edge",
            style: {
              width: 2,
              "line-color": "#ccc",
              "target-arrow-color": "#ccc",
              "target-arrow-shape": "triangle",
              label: "data(label)",
              "font-size": "10px",
              "text-background-color": "#fff",
              "text-background-opacity": 0.8
            },
          },
          {
            selector: ".highlighted",
            style: {
              "background-color": "#ff0000",
              "border-width": 3,
              "border-color": "#000"
            }
          }
        ],
        layout: {
          name: "cose-bilkent",
          animate: true,
          animationDuration: 1000
        },
      });

      // Add click handlers for node details
      cy.on('tap', 'node', function(evt) {
        const node = evt.target;
        console.log('Node tapped:', node.data());
        // Highlight connected nodes
        cy.elements().removeClass('highlighted');
        node.addClass('highlighted');
        node.neighborhood().addClass('highlighted');
      });

      return () => cy.destroy();
    }
  }, [nodes, edges]);

  const handleSearch = () => {
    if (searchQuery.trim()) {
      fetch(`/api/kg/search?q=${encodeURIComponent(searchQuery)}`)
        .then((res) => res.json())
        .then((data) => {
          // Update visualization with search results
          console.log("Search results:", data);
          // For now, just log; in full implementation, update nodes/edges
        })
        .catch((err) => console.error("Search error:", err));
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Knowledge Graph Studio</h1>

      {/* KG Statistics */}
      <div style={{ marginBottom: "20px", padding: "10px", backgroundColor: "#f5f5f5", borderRadius: "5px" }}>
        <h3>Knowledge Graph Statistics</h3>
        <p>Total Nodes: {kgStats.total_nodes || 0}</p>
        <p>Total Edges: {kgStats.total_edges || 0}</p>
        <p>Average Connections: {kgStats.avg_connections ? kgStats.avg_connections.toFixed(2) : 0}</p>
      </div>

      {/* Search Bar */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Search knowledge graph..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{ padding: "8px", width: "300px", marginRight: "10px" }}
        />
        <button onClick={handleSearch} style={{ padding: "8px 16px" }}>Search</button>
      </div>

      {/* Filters */}
      <FilterPanel filter={filter} setFilter={setFilter} nodes={nodes} edges={edges} />

      {/* Cytoscape Container */}
      <div
        ref={cyRef}
        style={{ width: "100%", height: "600px", border: "1px solid #ccc", borderRadius: "5px" }}
      ></div>

      {/* Instructions */}
      <div style={{ marginTop: "20px", padding: "10px", backgroundColor: "#e8f4f8", borderRadius: "5px" }}>
        <h4>Instructions</h4>
        <ul>
          <li>Click on nodes to highlight connections</li>
          <li>Use filters to focus on specific node types or relationships</li>
          <li>Search for specific terms to find relevant graph elements</li>
          <li>Proof tokens are embedded in edge data for verification</li>
        </ul>
      </div>
    </div>
  );
}
