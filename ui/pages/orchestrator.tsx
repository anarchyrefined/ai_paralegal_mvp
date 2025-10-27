import React, { useState, useEffect } from "react";
import FormAgentSelector from "../components/FormAgentSelector";
import LogConsole from "../components/LogConsole";
import { runTask } from "../lib/api";

export default function OrchestratorPage() {
  const [task, setTask] = useState("");
  const [params, setParams] = useState("{}");
  const [agent, setAgent] = useState("");
  const [jobInfo, setJobInfo] = useState<{ id: string; statusUrl: string } | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await runTask({
        task,
        agent,
        paramsJSON: params,
      });
      setJobInfo(res);
    } finally {
        setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#1E1E1E] text-gray-100 p-6 space-y-6">
      <header className="flex items-start justify-between">
        <section>
          <h1 className="text-xl font-semibold text-white">Task Orchestrator</h1>
          <p className="text-sm text-gray-400">
            Submit work to repo agents and track execution
          </p>
        </section>
      </header>

      <form
        onSubmit={handleSubmit}
        className="bg-[#2C2C2C] border border-[#3A3A3A] rounded-lg p-4 space-y-4 max-w-3xl"
      >
        <div className="flex flex-col gap-2">
          <label className="text-sm text-gray-300 font-medium">Task description</label>
          <textarea
            className="bg-[#1E1E1E] border border-[#3A3A3A] rounded-md p-3 text-sm text-gray-100 min-h-[100px] focus:outline-none focus:ring-1 focus:ring-emerald-600"
            placeholder="Analyze contract disputes involving Party A and Party B..."
            value={task}
            onChange={(e) => setTask(e.target.value)}
            required
          />
        </div>

        <div className="flex flex-col gap-2">
          <label className="text-sm text-gray-300 font-medium">Agent / Strategy</label>
          <FormAgentSelector value={agent} onChange={setAgent} />
        </div>

        <div className="flex flex-col gap-2">
          <label className="text-sm text-gray-300 font-medium">Parameters (JSON)</label>
          <textarea
            className="bg-[#1E1E1E] border border-[#3A3A3A] rounded-md p-3 text-sm text-gray-100 min-h-[80px] font-mono text-xs"
            value={params}
            onChange={(e) => setParams(e.target.value)}
          />
          <p className="text-[10px] text-gray-500">
            Example: {"{ \"limit\": 200, \"maskPII\": true }"}
          </p>
        </div>

        <button
          type="submit"
          className="px-3 py-2 rounded-md bg-emerald-600 text-sm font-medium disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Submitting..." : "Submit Task"}
        </button>

        {jobInfo && (
          <div className="bg-[#1E1E1E] border border-[#3A3A3A] rounded-md p-3 text-xs text-gray-200 space-y-1">
            <div className="flex items-center justify-between">
              <span className="font-medium text-gray-100">Job ID</span>
              <code className="font-mono text-emerald-400">{jobInfo.id}</code>
            </div>
            <div className="flex items-center justify-between">
              <span className="font-medium text-gray-100">Status URL</span>
              <a
                className="font-mono text-emerald-400 underline break-all"
                href={jobInfo.statusUrl}
              >
                {jobInfo.statusUrl}
              </a>
            </div>
            <p className="text-gray-400 pt-2">Task submitted successfully</p>
          </div>
        )}
      </form>

      <section className="bg-[#2C2C2C] border border-[#3A3A3A] rounded-lg p-4">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-medium text-gray-200">Execution Log</h2>
          <span className="text-[10px] text-gray-500">realtime</span>
        </div>
        <LogConsole />
      </section>
    </main>
  );
}
