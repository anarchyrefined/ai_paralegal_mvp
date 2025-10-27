import React, { useEffect, useState } from "react";
import { fetchAgents } from "../lib/api";

export default function FormAgentSelector({
  value,
  onChange,
}: {
  value: string;
  onChange: (v: string) => void;
}) {
  const [agents, setAgents] = useState<string[]>([]);

  useEffect(() => {
    async function load() {
      const list = await fetchAgents();
      setAgents(list);
    }
    load();
  }, []);

  return (
    <select
      className="bg-[#1E1E1E] border border-[#3A3A3A] rounded-md p-3 text-sm text-gray-100 focus:outline-none focus:ring-1 focus:ring-emerald-600"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      required
    >
      <option value="">Select agent…</option>
      {agents.map((agent) => (
        <option key={agent} value={agent}>
          {agent}
        </option>
      ))}
    </select>
  );
}
