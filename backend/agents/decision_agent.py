"""Decision Agent"""
from agents.base_agent import BaseAgent
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage


class DecisionAgent(BaseAgent):
    role = "decision"
    goal = "Analyse data and agent outputs to recommend the best strategy"
    tools = ["data_analyser", "rag_retriever"]

    def _build_system_prompt(self, rag_context: str) -> str:
        return f"""You are the Decision Agent — a strategic analyst and product advisor.
Synthesise all available information into clear, actionable recommendations.
Context: {rag_context}"""

    async def _act(self, thought: dict, input: str, context: dict) -> dict:
        messages = [
            SystemMessage(content=self._build_system_prompt("")),
            HumanMessage(content=f"Make a strategic decision for: {input}\n\nContext: {context}\n\nRespond as JSON: {{\"recommendation\": \"...\", \"options\": [], \"risks\": [], \"next_steps\": []}}"),
        ]
        response = await self.llm.agenerate([messages])
        return self._parse_json(response.generations[0][0].text)

    async def synthesise(self, goal: str, agent_results: Dict[str, Any]) -> dict:
        """Final synthesis of all agent outputs into one cohesive answer."""
        messages = [
            SystemMessage(content="You are the Decision Agent. Synthesise all agent work into a clear final answer for the user."),
            HumanMessage(content=f"Goal: {goal}\n\nAll agent results:\n{agent_results}\n\nWrite a comprehensive final answer. JSON: {{\"summary\": \"...\", \"key_deliverables\": [], \"next_steps\": []}}"),
        ]
        response = await self.llm.agenerate([messages])
        return self._parse_json(response.generations[0][0].text)
