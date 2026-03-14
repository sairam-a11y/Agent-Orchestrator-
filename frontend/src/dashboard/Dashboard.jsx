export default function Dashboard({ agents, onStart }) {
  const stack = [
    { layer: "User Interface", tech: "React + Next.js", color: "#7F77DD" },
    { layer: "API Gateway", tech: "FastAPI (Python)", color: "#378ADD" },
    { layer: "Agent Orchestrator", tech: "LangChain + CrewAI", color: "#1D9E75" },
    { layer: "Tool Layer", tech: "Web Search · Code Exec · File I/O · APIs", color: "#BA7517" },
    { layer: "Memory Layer", tech: "Short-term + Vector DB (Chroma)", color: "#D85A30" },
    { layer: "RAG Knowledge", tech: "Embeddings + Retriever Pipeline", color: "#D4537E" },
    { layer: "Databases", tech: "PostgreSQL · Redis · ChromaDB", color: "#639922" },
  ];

  const stats = [
    { label: "Agents", value: "8" },
    { label: "Tools", value: "5" },
    { label: "Memory Types", value: "2" },
    { label: "RAG Pipeline", value: "✓" },
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      {/* Hero */}
      <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "2rem" }}>
        <p style={{ fontSize: 11, fontWeight: 500, color: "var(--color-text-tertiary)", textTransform: "uppercase", letterSpacing: "0.1em", margin: "0 0 8px" }}>Universal</p>
        <h1 style={{ fontSize: 28, fontWeight: 600, margin: "0 0 0.5rem", letterSpacing: "-0.5px" }}>Agentic AI Platform</h1>
        <p style={{ fontSize: 15, color: "var(--color-text-secondary)", margin: "0 0 1.5rem", maxWidth: 500, lineHeight: 1.6 }}>
          Multi-agent system where specialised AI agents collaborate autonomously — with tool use, memory, and RAG knowledge retrieval.
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: "1.5rem" }}>
          {stats.map((s) => (
            <div key={s.label} style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "0.75rem 1rem" }}>
              <p style={{ fontSize: 22, fontWeight: 600, margin: "0 0 2px", fontFamily: "var(--font-mono)" }}>{s.value}</p>
              <p style={{ fontSize: 12, color: "var(--color-text-tertiary)", margin: 0 }}>{s.label}</p>
            </div>
          ))}
        </div>
        <button onClick={onStart}
          style={{ padding: "10px 24px", borderRadius: "var(--border-radius-md)", border: "none", background: "var(--color-text-primary)", color: "var(--color-background-primary)", fontWeight: 500, fontSize: 14, cursor: "pointer", fontFamily: "inherit" }}>
          Launch Agent Run ↗
        </button>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.5rem" }}>
        {/* Architecture stack */}
        <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "1.25rem" }}>
          <p style={{ fontSize: 13, fontWeight: 500, margin: "0 0 1rem" }}>System Architecture</p>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            {stack.map((s, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                {i > 0 && (
                  <div style={{ position: "absolute" }} />
                )}
                <div style={{ width: 3, height: 28, background: s.color, borderRadius: 2, flexShrink: 0 }} />
                <div style={{ flex: 1 }}>
                  <p style={{ margin: 0, fontSize: 13, fontWeight: 500 }}>{s.layer}</p>
                  <p style={{ margin: 0, fontSize: 11, color: "var(--color-text-tertiary)" }}>{s.tech}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Agents grid */}
        <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "1.25rem" }}>
          <p style={{ fontSize: 13, fontWeight: 500, margin: "0 0 1rem" }}>Agents</p>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
            {agents.map((a) => (
              <div key={a.id} style={{ padding: "10px 12px", borderRadius: "var(--border-radius-md)", border: "0.5px solid var(--color-border-tertiary)", display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ fontSize: 18 }}>{a.icon}</span>
                <div>
                  <p style={{ margin: 0, fontSize: 13, fontWeight: 500 }}>{a.label}</p>
                  <p style={{ margin: 0, fontSize: 11, color: "var(--color-text-tertiary)" }}>Agent</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Demo flow */}
      <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "1.25rem" }}>
        <p style={{ fontSize: 13, fontWeight: 500, margin: "0 0 1rem" }}>Hackathon Demo Flow</p>
        <div style={{ display: "flex", alignItems: "center", gap: 0, overflowX: "auto" }}>
          {["Planner", "Research", "Developer", "Debug", "Website", "Decision"].map((name, i, arr) => (
            <div key={name} style={{ display: "flex", alignItems: "center" }}>
              <div style={{ padding: "8px 14px", borderRadius: "var(--border-radius-md)", background: "var(--color-background-secondary)", fontSize: 12, fontWeight: 500, whiteSpace: "nowrap" }}>
                {name}
              </div>
              {i < arr.length - 1 && (
                <span style={{ fontSize: 16, color: "var(--color-text-tertiary)", padding: "0 4px" }}>→</span>
              )}
            </div>
          ))}
        </div>
        <p style={{ fontSize: 12, color: "var(--color-text-tertiary)", margin: "8px 0 0" }}>
          Input: "Build a SaaS productivity tool" → Full plan, code, landing page, pricing strategy
        </p>
      </div>
    </div>
  );
}
