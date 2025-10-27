import React, { useState } from "react";

export default function SettingsPage() {
  const [apiKey, setApiKey] = useState("");
  const [statusMsg, setStatusMsg] = useState("");

  async function testConnection() {
    // call /api/health on backend FastAPI
    try {
      const res = await fetch("/api/health");
      const data = await res.json();
      setStatusMsg(`Backend status: ${data.status}`);
    } catch (err) {
      setStatusMsg("Error: cannot reach backend");
    }
  }

  return (
    <main className="min-h-screen bg-[#1E1E1E] text-gray-100 p-6 space-y-6">
      <header>
        <h1 className="text-xl font-semibold text-white">Settings</h1>
        <p className="text-sm text-gray-400">
          API keys and runtime diagnostics
        </p>
      </header>

      <section className="bg-[#2C2C2C] border border-[#3A3A3A] rounded-lg p-4 max-w-xl space-y-4">
        <div>
          <label className="block text-sm text-gray-300 font-medium mb-2">
            API key
          </label>
          <input
            className="w-full bg-[#1E1E1E] border border-[#3A3A3A] rounded-md p-3 text-sm text-gray-100 font-mono focus:outline-none focus:ring-1 focus:ring-emerald-600"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="sk-***"
          />
          <p className="text-[10px] text-gray-500 mt-2">
            This will be stored locally in encrypted storage.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            className="px-3 py-2 rounded-md bg-emerald-600 text-sm font-medium"
          >
            Save
          </button>
          <button
            type="button"
            onClick={testConnection}
            className="px-3 py-2 rounded-md bg-[#1E1E1E] border border-[#3A3A3A] text-sm font-medium"
          >
            Test Backend
          </button>
        </div>

        {statusMsg && (
          <div className="text-xs text-gray-200 font-mono bg-[#1E1E1E] border border-[#3A3A3A] rounded-md p-3">
            {statusMsg}
          </div>
        )}
      </section>
    </main>
  );
}
