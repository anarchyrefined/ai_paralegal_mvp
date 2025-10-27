"use client";
import React, { useEffect, useRef } from "react";
import cytoscape from "cytoscape";

export default function GraphPanel({
  onSelectNode,
  nodes,
  edges,
}: {
  onSelectNode: (n: any) => void;
  nodes?: any[];
  edges?: any[];
}) {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    async function init() {
      let graphData;
      if (nodes && edges) {
        graphData = { nodes, edges };
      } else {
        graphData = await fetch("/api/kg")
          .then((r) => r.json())
          .catch(() => ({
            nodes: [{ data: { id: "A", label: "Party A" } }],
            edges: [],
          }));
      }

      const cy = cytoscape({
        container: containerRef.current,
        style: [
          {
            selector: "node",
            style: {
              "background-color": "#10B981",
              color: "#FFFFFF",
              label: "data(label)",
              "font-size": "8px",
              "text-wrap": "wrap",
            },
          },
          {
            selector: "edge",
            style: {
              width: 1,
              "line-color": "#3A3A3A",
              "target-arrow-color": "#3A3A3A",
              "target-arrow-shape": "triangle",
              "curve-style": "bezier",
            },
          },
        ],
        elements: {
          nodes: graphData.nodes.map((n: any) => ({ data: n.data })),
          edges: graphData.edges.map((e: any) => ({ data: e.data })),
        },
        layout: { name: "cose", animate: false },
      });

      cy.on("tap", "node", (evt) => {
        const node = evt.target;
        onSelectNode({
          id: node.id(),
          label: node.data("label"),
          data: node.data(),
        });
      });
    }

    init();
  }, [onSelectNode, nodes, edges]);

  return <div className="w-full h-full" ref={containerRef} />;
}
