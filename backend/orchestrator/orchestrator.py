"""
Agent Orchestrator
------------------
Receives a user goal, decomposes it into tasks, assigns agents,
manages inter-agent communication, and aggregates results.
"""

import asyncio
from typing import Optional, List, Dict, Any
from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.developer_agent import DeveloperAgent
from agents.debug_agent import DebugAgent
from agents.website_agent import WebsiteAgent
from agents.legal_agent import LegalAgent
from agents.decision_agent import DecisionAgent
from agents.productivity_agent import ProductivityAgent
from memory.memory_manager import MemoryManager
from monitoring.logger import PlatformLogger


class AgentOrchestrator:
    """Central controller for the multi-agent platform."""

    def __init__(self):
        self.memory = MemoryManager()
        self.logger = PlatformLogger()

        # Register all agents
        self.agents: Dict[str, Any] = {
            "planner":    PlannerAgent(memory=self.memory),
            "research":   ResearchAgent(memory=self.memory),
            "developer":  DeveloperAgent(memory=self.memory),
            "debug":      DebugAgent(memory=self.memory),
            "website":    WebsiteAgent(memory=self.memory),
            "legal":      LegalAgent(memory=self.memory),
            "decision":   DecisionAgent(memory=self.memory),
            "productivity": ProductivityAgent(memory=self.memory),
        }

    def list_agents(self) -> List[dict]:
        return [
            {"name": name, "role": agent.role, "status": agent.status}
            for name, agent in self.agents.items()
        ]

    async def execute(
        self,
        goal: str,
        context: Optional[str] = None,
        agent_override: Optional[List[str]] = None,
    ) -> dict:
        """
        Main execution pipeline.
        1. Planner breaks goal into tasks
        2. Tasks are dispatched to relevant agents
        3. Results are combined and returned
        """
        self.logger.log_event("ORCHESTRATOR_START", {"goal": goal})

        # ── Step 1: Planning ──────────────────────────────────────────────────
        plan = await self.agents["planner"].run(
            input=goal,
            context=context or "",
        )
        self.logger.log_event("PLAN_CREATED", {"tasks": plan.get("tasks", [])})

        # ── Step 2: Dispatch tasks to agents ─────────────────────────────────
        tasks = plan.get("tasks", [])
        if agent_override:
            tasks = [t for t in tasks if t.get("agent") in agent_override]

        results: Dict[str, Any] = {}
        shared_context = {"goal": goal, "plan": plan}

        for task in tasks:
            agent_name = task.get("agent")
            if agent_name not in self.agents:
                self.logger.log_event("AGENT_NOT_FOUND", {"agent": agent_name})
                continue

            agent = self.agents[agent_name]
            self.logger.log_event("AGENT_START", {"agent": agent_name, "task": task})

            try:
                agent.status = "running"
                output = await agent.run(
                    input=task.get("description", ""),
                    context=shared_context,
                )
                results[agent_name] = output
                shared_context[agent_name + "_output"] = output  # pass forward
                agent.status = "idle"
                self.logger.log_event("AGENT_DONE", {"agent": agent_name})
            except Exception as e:
                results[agent_name] = {"error": str(e)}
                agent.status = "error"
                self.logger.log_event("AGENT_ERROR", {"agent": agent_name, "error": str(e)})

        # ── Step 3: Decision agent synthesises final answer ───────────────────
        final_output = await self.agents["decision"].synthesise(
            goal=goal,
            agent_results=results,
        )

        self.logger.log_event("ORCHESTRATOR_DONE", {"goal": goal})

        return {
            "plan": plan,
            "results": results,
            "final_output": final_output,
        }
