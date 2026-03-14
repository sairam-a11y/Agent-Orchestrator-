"""Productivity Agent"""
from agents.base_agent import BaseAgent
from langchain_core.messages import HumanMessage, SystemMessage


class ProductivityAgent(BaseAgent):
    role = "productivity"
    goal = "Schedule tasks, manage workflows, and optimise team productivity"
    tools = ["calendar_api", "task_manager", "file_system"]

    def _build_system_prompt(self, rag_context: str) -> str:
        return f"""You are the Productivity Agent — an expert project manager and workflow designer.
Create clear timelines, assign priorities, and identify blockers.
Context: {rag_context}"""

    async def _act(self, thought: dict, input: str, context: dict) -> dict:
        messages = [
            SystemMessage(content=self._build_system_prompt("")),
            HumanMessage(content=f"Create a productivity plan for: {input}\n\nRespond as JSON: {{\"timeline\": [], \"milestones\": [], \"blockers\": [], \"weekly_plan\": {{}}}}"),
        ]
        response = await self.llm.agenerate([messages])
        return self._parse_json(response.generations[0][0].text)
