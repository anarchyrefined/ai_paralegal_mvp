import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import GraphPanel from "../components/GraphPanel";
import FilterPanel from "../components/FilterPanel";

export default function KGPage() {
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [filter, setFilter] = useState({ nodeType: "", relationship: "", motive: "", context: "" });
  const [nodes, setNodes] = useState<any[]>([]);
  const [edges, setEdges] = useState<any[]>([]);

  useEffect(() => {
    async function fetchGraphData() {
      try {
        const graphData = await fetch("/api/kg").then((r) => r.json());
        setNodes(graphData.nodes || []);
        setEdges(graphData.edges || []);
      } catch (err) {
        console.error("Failed to fetch graph data:", err);
        setNodes([{ data: { id: "A", label: "Party A" } }]);
        setEdges([]);
      }
    }
    fetchGraphData();
  }, []);

  const applyFilter = (newFilter: typeof filter) => {
    setFilter(newFilter);
  };

  const filteredNodes = nodes.filter((node) => {
    if (filter.nodeType && node.data.type !== filter.nodeType) return false;
    if (filter.motive && node.data.type === "Motive" && !node.data.label.toLowerCase().includes(filter.motive.toLowerCase())) return false;
    if (filter.context && node.data.type === "Context" && !node.data.label.toLowerCase().includes(filter.context.toLowerCase())) return false;
    return true;
  });

  const filteredEdges = edges.filter((edge) => {
    if (filter.relationship && edge.data.label !== filter.relationship) return false;
    return true;
  });

  return (
    <main className="min-h-screen bg-[#1E1E1E] text-gray-100 p-6 space-y-6">
      <header>
        <h1 className="text-xl font-semibold text-white">Knowledge Graph</h1>
        <p className="text-sm text-gray-400">
          Explore entities, links, and evidence
        </p>
      </header>

      <FilterPanel filter={filter} setFilter={setFilter} onApply={applyFilter} />

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-[#2C2C2C] border border-[#3A3A3A] rounded-lg p-2 h-[480px]">
          <GraphPanel onSelectNode={setSelectedNode} nodes={filteredNodes} edges={filteredEdges} />
        </div>

        <aside className="bg-[#2C2C2C] border border-[#3A3A3A] rounded-lg p-4 text-sm space-y-2 h-[480px] overflow-y-auto">
          <h2 className="text-gray-200 font-medium flex items-center justify-between">
            Node details
            <span className="text-[10px] text-gray-500 font-normal">read only</span>
          </h2>

          {selectedNode ? (
            <>
              <div>
                <div className="text-[10px] uppercase text-gray-500">ID</div>
                <div className="font-mono text-xs text-emerald-400 break-all">
                  {selectedNode.id}
                </div>
              </div>

              <div>
                <div className="text-[10px] uppercase text-gray-500">Label</div>
                <div className="text-gray-200">{selectedNode.label}</div>
              </div>

              <div>
                <div className="text-[10px] uppercase text-gray-500">Metadata</div>
                <pre className="bg-[#1E1E1E] border border-[#3A3A3A] rounded-md p-2 text-[10px] leading-relaxed text-gray-300 whitespace-pre-wrap break-words">
{JSON.stringify(selectedNode.data, null, 2)}
                </pre>
              </div>
            </>
          ) : (
            <p className="text-gray-500 text-xs">Select a node to inspect metadata</p>
          )}
        </aside>
      </section>
    </main>
  );
}
