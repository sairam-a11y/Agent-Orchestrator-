"""
Planner Agent
-------------
Breaks user goals into structured task plans and assigns agents.
"""
from agents.base_agent import BaseAgent
from langchain_core.messages import HumanMessage, SystemMessage


class PlannerAgent(BaseAgent):
    role = "planner"
    goal = "Break complex user goals into structured, executable task plans"
    tools = ["task_decomposer", "agent_router"]

    def _build_system_prompt(self, rag_context: str) -> str:
        return f"""You are the Planner Agent. Your sole job is to decompose a user goal
into a list of tasks, each assigned to the most suitable agent.

Available agents: planner, research, developer, debug, website, legal, decision, productivity

Knowledge context:
{rag_context}

Always respond with valid JSON.
"""

    async def _act(self, thought: dict, input: str, context: dict) -> dict:
        messages = [
            SystemMessage(content=self._build_system_prompt("")),
            HumanMessage(content=f"""
Goal: {input}

Create a task plan. Respond as JSON:
{{
  "tasks": [
    {{"id": 1, "description": "...", "agent": "research", "depends_on": []}},
    {{"id": 2, "description": "...", "agent": "developer", "depends_on": [1]}}
  ],
  "estimated_agents": ["research", "developer"],
  "rationale": "..."
}}
"""),
        ]
        response = await self.llm.agenerate([messages])
        return self._parse_json(response.generations[0][0].text)
