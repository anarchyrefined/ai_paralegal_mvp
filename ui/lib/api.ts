export async function fetchAgents(): Promise<string[]> {
  try {
    const res = await fetch("/api/personas");
    if (!res.ok) {
      throw new Error(`Failed to fetch agents: ${res.status} ${res.statusText}`);
    }
    const data = await res.json();
    return data.personas || [];
  } catch (err) {
    console.error("Failed to fetch agents:", err);
    return [];
  }
}

export async function runTask(params: { task: string; agent: string; paramsJSON: string }) {
  try {
    const res = await fetch("/api/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params),
    });
    if (!res.ok) {
      throw new Error(`Failed to run task: ${res.status} ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    console.error("Failed to run task:", err);
    throw err; // Re-throw to let caller handle
  }
}
