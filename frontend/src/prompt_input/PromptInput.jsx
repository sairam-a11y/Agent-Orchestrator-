export default function PromptInput({ goal, setGoal, onSubmit, status }) {
  const running = status === "running";

  const examples = [
    "Build a SaaS productivity tool",
    "Create a legal contract review system",
    "Develop an e-commerce platform with AI recommendations",
    "Build a real-time analytics dashboard",
  ];

  return (
    <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "1.25rem" }}>
      <p style={{ fontSize: 14, fontWeight: 500, margin: "0 0 0.75rem" }}>What do you want to build?</p>
      <textarea
        value={goal}
        onChange={(e) => setGoal(e.target.value)}
        disabled={running}
        placeholder="e.g. Build a SaaS productivity tool with task management, team collaboration, and analytics..."
        rows={3}
        style={{ width: "100%", resize: "vertical", boxSizing: "border-box", fontSize: 14, padding: "0.75rem", borderRadius: "var(--border-radius-md)", border: "0.5px solid var(--color-border-secondary)", background: "var(--color-background-secondary)", color: "var(--color-text-primary)", fontFamily: "inherit", lineHeight: 1.5 }}
        onKeyDown={(e) => { if (e.key === "Enter" && e.metaKey) onSubmit(); }}
      />
      <div style={{ display: "flex", gap: 8, marginTop: "0.75rem", flexWrap: "wrap" }}>
        {examples.map((ex) => (
          <button key={ex} onClick={() => setGoal(ex)} disabled={running}
            style={{ fontSize: 11, padding: "4px 10px", borderRadius: 20, border: "0.5px solid var(--color-border-secondary)", background: "var(--color-background-secondary)", cursor: "pointer", color: "var(--color-text-secondary)" }}>
            {ex}
          </button>
        ))}
      </div>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: "1rem" }}>
        <span style={{ fontSize: 12, color: "var(--color-text-tertiary)" }}>⌘ + Enter to run</span>
        <button onClick={onSubmit} disabled={running || !goal.trim()}
          style={{ padding: "8px 20px", borderRadius: "var(--border-radius-md)", border: "none", background: running ? "var(--color-background-secondary)" : "var(--color-text-primary)", color: running ? "var(--color-text-secondary)" : "var(--color-background-primary)", fontWeight: 500, fontSize: 14, cursor: running ? "not-allowed" : "pointer", fontFamily: "inherit" }}>
          {running ? "⏳ Running agents..." : "Run Agents ↗"}
        </button>
      </div>
    </div>
  );
}
