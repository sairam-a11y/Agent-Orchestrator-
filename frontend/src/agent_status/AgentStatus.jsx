export default function AgentStatus({ agents, states }) {
  const statusColor = {
    idle:    "var(--color-text-tertiary)",
    running: "#EF9F27",
    done:    "#1D9E75",
    error:   "#E24B4A",
  };

  const statusLabel = {
    idle: "idle", running: "running", done: "done", error: "error"
  };

  const completed = Object.values(states).filter((s) => s === "done").length;
  const total = agents.length;
  const pct = Math.round((completed / total) * 100);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      {/* Progress */}
      <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "1.25rem" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
          <p style={{ fontSize: 13, fontWeight: 500, margin: 0 }}>Progress</p>
          <span style={{ fontSize: 13, fontWeight: 500, fontFamily: "var(--font-mono)" }}>{pct}%</span>
        </div>
        <div style={{ height: 4, background: "var(--color-background-secondary)", borderRadius: 2, overflow: "hidden" }}>
          <div style={{ height: "100%", width: `${pct}%`, background: "#1D9E75", borderRadius: 2, transition: "width 0.5s ease" }} />
        </div>
        <p style={{ fontSize: 12, color: "var(--color-text-tertiary)", margin: "6px 0 0" }}>{completed} of {total} agents complete</p>
      </div>

      {/* Agent cards */}
      <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "1.25rem" }}>
        <p style={{ fontSize: 13, fontWeight: 500, margin: "0 0 1rem" }}>Agent Status</p>
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {agents.map((agent) => {
            const state = states[agent.id] || "idle";
            return (
              <div key={agent.id} style={{ display: "flex", alignItems: "center", gap: 10, padding: "8px 10px", borderRadius: "var(--border-radius-md)", background: state === "running" ? "var(--color-background-secondary)" : "transparent", transition: "background 0.3s" }}>
                <span style={{ fontSize: 16 }}>{agent.icon}</span>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <p style={{ margin: 0, fontSize: 13, fontWeight: 500 }}>{agent.label}</p>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 5 }}>
                  {state === "running" && (
                    <span style={{ display: "inline-block", width: 6, height: 6, borderRadius: "50%", background: "#EF9F27", animation: "pulse 1s ease-in-out infinite" }} />
                  )}
                  <span style={{ fontSize: 11, color: statusColor[state], fontFamily: "var(--font-mono)" }}>{statusLabel[state]}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.5; transform: scale(0.8); }
        }
      `}</style>
    </div>
  );
}
