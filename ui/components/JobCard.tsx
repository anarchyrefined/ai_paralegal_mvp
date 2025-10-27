import React from "react";

export default function JobCard({
  job,
}: {
  job: { id: string; agent: string; status: string; startedAt: string };
}) {
  return (
    <div className="bg-[#1E1E1E] border border-[#3A3A3A] rounded-md p-3 text-xs text-gray-200 flex flex-col md:flex-row md:items-center md:justify-between gap-2">
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <span className="font-mono text-emerald-400">{job.id}</span>
          <span
            className={
              "px-2 py-[2px] rounded-md text-[10px] font-medium " +
              (job.status === "success"
                ? "bg-emerald-600 text-white"
                : job.status === "running"
                ? "bg-yellow-600 text-white"
                : "bg-gray-600 text-white")
            }
          >
            {job.status}
          </span>
        </div>
        <div className="text-gray-400">
          Agent <span className="text-gray-200">{job.agent}</span>
        </div>
      </div>

      <div className="text-[10px] text-gray-500 md:text-right">
        <div>Started {job.startedAt}</div>
      </div>
    </div>
  );
}
