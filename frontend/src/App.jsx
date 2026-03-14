import { useState, useEffect, useRef } from "react";
import PromptInput from "./prompt_input/PromptInput";
import AgentStatus from "./agent_status/AgentStatus";
import Dashboard from "./dashboard/Dashboard";

const AGENTS = [
  { id: "planner",     label: "Planner",     color: "#7F77DD", icon: "🗺" },
  { id: "research",    label: "Research",    color: "#1D9E75", icon: "🔍" },
  { id: "developer",   label: "Developer",   color: "#378ADD", icon: "💻" },
  { id: "debug",       label: "Debug",       color: "#BA7517", icon: "🐛" },
  { id: "website",     label: "Website",     color: "#D4537E", icon: "🌐" },
  { id: "legal",       label: "Legal",       color: "#639922", icon: "⚖" },
  { id: "decision",    label: "Decision",    color: "#D85A30", icon: "🎯" },
  { id: "productivity",label: "Productivity",color: "#888780", icon: "📋" },
];

export default function App() {
  const [view, setView] = useState("dashboard"); // dashboard | run
  const [goal, setGoal] = useState("");
  const [taskId, setTaskId] = useState(null);
  const [taskResult, setTaskResult] = useState(null);
  const [status, setStatus] = useState("idle");
  const [logs, setLogs] = useState([]);
  const [agentStates, setAgentStates] = useState(
    Object.fromEntries(AGENTS.map((a) => [a.id, "idle"]))
  );
  const pollRef = useRef(null);

  const BASE = "http://localhost:8000";

  async function submitGoal() {
    if (!goal.trim()) return;
    setStatus("running");
    setTaskResult(null);
    setLogs([]);
    setView("run");

    // Reset all agents to idle then activate planner
    setAgentStates(Object.fromEntries(AGENTS.map((a) => [a.id, "idle"])));
    setAgentStates((s) => ({ ...s, planner: "running" }));
    addLog("system", `Goal submitted: "${goal}"`);

    try {
      const res = await fetch(`${BASE}/api/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal }),
      });
      const data = await res.json();
      setTaskId(data.task_id);
      addLog("system", `Task ID: ${data.task_id}`);
      pollRef.current = setInterval(() => pollTask(data.task_id), 2000);
    } catch (e) {
      // Demo mode: simulate agent workflow
      simulateDemoFlow();
    }
  }

  function addLog(agent, msg, time = new Date().toLocaleTimeString()) {
    setLogs((l) => {
      if (l.some(entry => entry.msg === msg && entry.agent === agent)) return l;
      return [...l, { agent, msg, time }];
    });
  }

  async function pollTask(id) {
    try {
      const res = await fetch(`${BASE}/api/task/${id}`);
      const data = await res.json();
      
      if (data.status === "completed" || data.status === "failed") {
        clearInterval(pollRef.current);
        setTaskResult(data);
        setStatus(data.status);
        setAgentStates(Object.fromEntries(AGENTS.map((a) => [a.id, "done"])));
        addLog("system", "Task execution finished.");
      }

      // Live update agent states and logs from backend logs
      const logRes = await fetch(`${BASE}/api/logs?limit=5`);
      const recentLogs = await logRes.json();
      recentLogs.forEach(entry => {
        if (entry.event === "AGENT_START") {
          const agent = entry.data.agent;
          setAgentStates(s => ({ ...s, [agent]: "running" }));
          addLog(agent, `Started task: ${entry.data.task?.description?.substring(0, 100)}...`);
        } else if (entry.event === "AGENT_DONE") {
          setAgentStates(s => ({ ...s, [entry.data.agent]: "done" }));
        }
      });
    } catch (_) {}
  }

  function simulateDemoFlow() {
    const flow = [
      { agent: "planner",     delay: 500,  msg: "Breaking goal into tasks..." },
      { agent: "research",    delay: 2000, msg: "Searching web for competitors & trends..." },
      { agent: "developer",   delay: 4500, msg: "Generating backend architecture & code..." },
      { agent: "debug",       delay: 7000, msg: "Reviewing code for bugs & security issues..." },
      { agent: "website",     delay: 9000, msg: "Creating landing page HTML/CSS..." },
      { agent: "legal",       delay: 11000,msg: "Checking compliance & GDPR requirements..." },
      { agent: "decision",    delay: 13000,msg: "Synthesising final strategy & pricing..." },
    ];
    flow.forEach(({ agent, delay, msg }) => {
      setTimeout(() => {
        setAgentStates((s) => ({ ...s, [agent]: "running" }));
        addLog(agent, msg);
        setTimeout(() => {
          setAgentStates((s) => ({ ...s, [agent]: "done" }));
          addLog(agent, "✓ Completed");
        }, 1800);
      }, delay);
    });
    setTimeout(() => {
      setStatus("completed");
      setTaskResult({
        status: "completed",
        final_output: {
          summary: "Your SaaS productivity platform has been fully designed.",
          key_deliverables: [
            "Task management system with Kanban + Calendar views",
            "React + FastAPI architecture with JWT auth",
            "Responsive landing page with hero, features & pricing sections",
            "Freemium pricing: Free / $12 Pro / $49 Team",
            "GDPR-compliant data handling checklist",
          ],
          next_steps: [
            "Set up GitHub repo and CI/CD pipeline",
            "Register domain and configure hosting",
            "Launch beta with 50 target users",
          ],
        },
      });
      setAgentStates((s) => ({ ...s, productivity: "done" }));
      addLog("system", "🎉 Platform run complete!");
    }, 15500);
  }

  return (
    <div style={{ fontFamily: "'DM Sans', sans-serif", minHeight: "100vh", background: "var(--color-background-tertiary)" }}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet" />
      {/* Header */}
      <header style={{ background: "var(--color-background-primary)", borderBottom: "0.5px solid var(--color-border-tertiary)", padding: "0 2rem", display: "flex", alignItems: "center", gap: "2rem", height: 56 }}>
        <span style={{ fontWeight: 600, fontSize: 18, letterSpacing: "-0.5px" }}>⚡ AgentOS</span>
        <nav style={{ display: "flex", gap: "1.5rem" }}>
          {["dashboard", "run"].map((v) => (
            <button key={v} onClick={() => setView(v)}
              style={{ background: "none", border: "none", cursor: "pointer", fontSize: 14, fontWeight: view === v ? 500 : 400, color: view === v ? "var(--color-text-primary)" : "var(--color-text-secondary)", borderBottom: view === v ? "2px solid var(--color-text-primary)" : "2px solid transparent", padding: "4px 0" }}>
              {v === "dashboard" ? "Dashboard" : "Run Agent"}
            </button>
          ))}
        </nav>
        <span style={{ marginLeft: "auto", fontSize: 12, color: "var(--color-text-tertiary)", fontFamily: "var(--font-mono)" }}>8 agents · RAG · Memory</span>
      </header>

      <main style={{ padding: "2rem", maxWidth: 1200, margin: "0 auto" }}>
        {view === "dashboard" ? (
          <Dashboard agents={AGENTS} onStart={() => setView("run")} />
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 340px", gap: "1.5rem" }}>
            <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
              <PromptInput goal={goal} setGoal={setGoal} onSubmit={submitGoal} status={status} />
              {taskResult && <ResultPanel result={taskResult} />}
              <LogPanel logs={logs} />
            </div>
            <AgentStatus agents={AGENTS} states={agentStates} />
          </div>
        )}
      </main>
    </div>
  );
}

function ResultPanel({ result }) {
  const out = result?.final_output || result?.results || {};
  return (
    <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "1.25rem" }}>
      <p style={{ fontSize: 14, fontWeight: 500, margin: "0 0 1rem" }}>Final Output</p>
      {out.summary && <p style={{ fontSize: 14, color: "var(--color-text-secondary)", margin: "0 0 1rem", lineHeight: 1.6 }}>{out.summary}</p>}
      {out.key_deliverables?.length > 0 && (
        <>
          <p style={{ fontSize: 12, fontWeight: 500, color: "var(--color-text-tertiary)", margin: "0 0 8px", textTransform: "uppercase", letterSpacing: "0.05em" }}>Deliverables</p>
          <ul style={{ margin: "0 0 1rem", paddingLeft: "1.25rem" }}>
            {out.key_deliverables.map((d, i) => <li key={i} style={{ fontSize: 13, color: "var(--color-text-secondary)", marginBottom: 4 }}>{d}</li>)}
          </ul>
        </>
      )}
      {out.next_steps?.length > 0 && (
        <>
          <p style={{ fontSize: 12, fontWeight: 500, color: "var(--color-text-tertiary)", margin: "0 0 8px", textTransform: "uppercase", letterSpacing: "0.05em" }}>Next Steps</p>
          <ol style={{ margin: "0 0 1rem", paddingLeft: "1.25rem" }}>
            {out.next_steps.map((s, i) => <li key={i} style={{ fontSize: 13, color: "var(--color-text-secondary)", marginBottom: 4 }}>{s}</li>)}
          </ol>
        </>
      )}
      <div style={{ marginTop: "1rem", paddingTop: "1rem", borderTop: "0.5px solid var(--color-border-tertiary)", fontSize: 12, color: "var(--color-text-tertiary)", display: "flex", alignItems: "center", gap: 6 }}>
        <span>📂</span> <span>Files saved to: <code>backend/output/</code></span>
      </div>
    </div>
  );
}

function LogPanel({ logs }) {
  const ref = useRef(null);
  useEffect(() => { if (ref.current) ref.current.scrollTop = ref.current.scrollHeight; }, [logs]);
  return (
    <div style={{ background: "#111", borderRadius: "var(--border-radius-lg)", padding: "1rem", fontFamily: "var(--font-mono)", fontSize: 12 }}>
      <p style={{ color: "#888", margin: "0 0 8px", fontSize: 11, textTransform: "uppercase", letterSpacing: "0.05em" }}>Agent Logs</p>
      <div ref={ref} style={{ maxHeight: 220, overflowY: "auto", display: "flex", flexDirection: "column", gap: 4 }}>
        {logs.length === 0 && <span style={{ color: "#555" }}>Awaiting input...</span>}
        {logs.map((l, i) => (
          <div key={i} style={{ display: "flex", gap: 8 }}>
            <span style={{ color: "#555", minWidth: 60 }}>{l.time}</span>
            <span style={{ color: "#7F77DD", minWidth: 80 }}>[{l.agent}]</span>
            <span style={{ color: "#c9c9c9" }}>{l.msg}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
