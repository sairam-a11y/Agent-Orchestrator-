from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
from typing import Optional, List
import uuid
import asyncio
from orchestrator.orchestrator import AgentOrchestrator
from monitoring.logger import PlatformLogger

app = FastAPI(
    title="Universal Agentic AI Platform",
    description="Multi-agent AI system with RAG, memory, and tool use",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = PlatformLogger()
orchestrator = AgentOrchestrator()

# ─── Request / Response Models ────────────────────────────────────────────────

class GoalRequest(BaseModel):
    goal: str
    context: Optional[str] = None
    agents: Optional[List[str]] = None  # override which agents to use

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class TaskResult(BaseModel):
    task_id: str
    status: str
    plan: Optional[dict] = None
    results: Optional[dict] = None
    error: Optional[str] = None

# ─── In-memory task store (replace with Redis in prod) ───────────────────────
task_store: dict = {}

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"message": "Universal Agentic AI Platform", "status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy", "agents": orchestrator.list_agents()}

@app.post("/api/run", response_model=TaskResponse)
async def run_goal(request: GoalRequest, background_tasks: BackgroundTasks):
    """Submit a goal for multi-agent execution."""
    task_id = str(uuid.uuid4())
    task_store[task_id] = {"status": "queued", "goal": request.goal}
    background_tasks.add_task(execute_goal, task_id, request)
    logger.log_event("TASK_CREATED", {"task_id": task_id, "goal": request.goal})
    return TaskResponse(task_id=task_id, status="queued", message="Task queued for execution")

@app.get("/api/task/{task_id}", response_model=TaskResult)
async def get_task(task_id: str):
    """Poll task status and results."""
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail="Task not found")
    task = task_store[task_id]
    return TaskResult(
        task_id=task_id,
        status=task.get("status"),
        plan=task.get("plan"),
        results=task.get("results"),
        error=task.get("error"),
    )

@app.get("/api/agents")
async def list_agents():
    """Return available agents and their status."""
    return orchestrator.list_agents()

@app.post("/api/documents/upload")
async def upload_document(content: str, source: str = "user"):
    """Ingest a document into the RAG knowledge base."""
    from rag.rag_pipeline import DocumentLoader
    loader = DocumentLoader()
    doc_id = await loader.ingest(content, source=source)
    return {"doc_id": doc_id, "status": "indexed"}

@app.get("/api/logs")
async def get_logs(limit: int = 50):
    """Retrieve recent platform logs."""
    return logger.recent_logs(limit)

# ─── Background task executor ────────────────────────────────────────────────

async def execute_goal(task_id: str, request: GoalRequest):
    task_store[task_id]["status"] = "running"
    try:
        result = await orchestrator.execute(
            goal=request.goal,
            context=request.context,
            agent_override=request.agents,
        )
        task_store[task_id].update({"status": "completed", **result})
        logger.log_event("TASK_COMPLETED", {"task_id": task_id})
    except Exception as e:
        task_store[task_id]["status"] = "failed"
        task_store[task_id]["error"] = str(e)
        logger.log_event("TASK_FAILED", {"task_id": task_id, "error": str(e)})
