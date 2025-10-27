import React from "react";
import Link from "next/link";
import JobCard from "../components/JobCard";
import LogConsole from "../components/LogConsole";

export default function DashboardPage() {
  // placeholder data
  const jobs = [
    { id: "job_123", agent: "ContractAnalysisAgent", status: "running", startedAt: "2025-10-27T01:24" },
    { id: "job_122", agent: "KGIngestor", status: "success", startedAt: "2025-10-27T01:10" },
  ];

  return (
    <main className="min-h-screen bg-[#1E1E1E] text-gray-100 p-6 space-y-6">
      <header className="flex items-start justify-between">
        <section>
          <h1 className="text-xl font-semibold text-white">Control Panel</h1>
          <p className="text-sm text-gray-400">codex-cli runtime overview</p>
        </section>

        <nav className="flex gap-3">
          <Link href="/orchestrator" className="px-3 py-2 rounded-md bg-emerald-600 text-sm font-medium">
            Run Task
          </Link>
          <Link href="/kg" className="px-3 py-2 rounded-md bg-[#2C2C2C] border border-[#3A3A3A] text-sm font-medium">
            Knowledge Graph
          </Link>
          <Link href="/settings" className="px-3 py-2 rounded-md bg-[#2C2C2C] border border-[#3A3A3A] text-sm font-medium">
            Settings
          </Link>
        </nav>
      </header>

      {/* Stats + quick actions */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-[#2C2C2C] border border-[#3A3A3A] rounded-lg p-4">
          <h2 className="text-sm font-medium text-gray-200 mb-2">Active Agents</h2>
          <p className="text-3xl font-semibold text-white leading-none">4</p>
          <p className="text-xs text-gray-500 mt-1">online</p>
        </div>

        <div className="bg-[#2C2C2C] border border-[#3A3A3A] rounded-lg p-4">
          <h2 className="text-sm font-medium text-gray-200 mb-2">Queue</h2>
          <p className="text-3xl font-semibold text-white leading-none">2</p>
          <p className="text-xs text-gray-500 mt-1">pending jobs</p>
        </div>

        <div className="bg-[#2C2C2C] border border-[#3A3A3A] rounded-lg p-4">
          <h2 className="text-sm font-medium text-gray-200 mb-3">Quick Actions</h2>
          <div className="flex flex-wrap gap-2">
            <Link
              href="/orchestrator"
              className="text-xs bg-emerald-600 hover:bg-emerald-500 px-3 py-2 rounded-md font-medium"
            >
              New Task
            </Link>
            <button className="text-xs bg-[#1E1E1E] border border-[#3A3A3A] px-3 py-2 rounded-md font-medium">
              Import Dataset
            </button>
            <button className="text-xs bg-[#1E1E1E] border border-[#3A3A3A] px-3 py-2 rounded-md font-medium">
              Launch Agent
            </button>
          </div>
        </div>
      </section>

      {/* Recent Jobs */}
      <section className="bg-[#2C2C2C] border border-[#3A3A3A] rounded-lg p-4">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-medium text-gray-200">Recent Jobs</h2>
          <Link className="text-xs text-emerald-500 hover:text-emerald-400" href="/orchestrator">
            View all
          </Link>
        </div>

        <div className="space-y-2">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      </section>

      {/* Logs */}
      <section className="bg-[#2C2C2C] border border-[#3A3A3A] rounded-lg p-4">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-medium text-gray-200">Live Logs</h2>
          <span className="text-[10px] text-gray-500">/ws stream</span>
        </div>
        <LogConsole />
      </section>
    </main>
  );
}
