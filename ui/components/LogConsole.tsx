import React, { useEffect, useState } from "react";

export default function LogConsole() {
  const [lines, setLines] = useState<string[]>([
    "[01:24:10] INFO  ContractAnalysisAgent starting…",
    "[01:24:11] MASK  PII masked for party identifiers",
    "[01:24:13] DONE  graph nodes updated (12 new edges)",
  ]);

  useEffect(() => {
    // TODO: replace with WebSocket(`/ws`)
    // ws.onmessage = ev => setLines(prev => [...prev, ev.data])
  }, []);

  return (
    <div className="bg-[#1E1E1E] border border-[#3A3A3A] rounded-md p-3 h-48 overflow-y-auto text-[10px] font-mono leading-relaxed text-gray-300">
      {lines.map((l, i) => (
        <div key={i}>{l}</div>
      ))}
    </div>
  );
}
