"""
Base Agent
----------
All agents inherit from this class.
Implements the Thought → Action → Observation → Reflection → Next Action loop.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from rag.rag_pipeline import RAGRetriever
from memory.memory_manager import MemoryManager
from monitoring.logger import PlatformLogger
import os
from dotenv import load_dotenv
load_dotenv()


class BaseAgent(ABC):
    """Abstract base for all platform agents."""

    role: str = "agent"
    goal: str = ""
    tools: list = []
    status: str = "idle"

    def __init__(self, memory: MemoryManager):
        self.memory = memory
        self.logger = PlatformLogger()
        self.retriever = RAGRetriever()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.3,
        )

    # ── Reasoning loop ────────────────────────────────────────────────────────

    async def run(self, input: str, context: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Execute the agent's reasoning loop."""
        self.logger.log_event(f"{self.role.upper()}_RUN", {"input": input[:120]})

        # Retrieve relevant knowledge from RAG
        rag_context = await self.retriever.retrieve(input)

        # Short-term memory: last N turns
        history = self.memory.get_short_term(self.role, n=5)

        # Build system prompt
        system_prompt = self._build_system_prompt(rag_context=rag_context)

        # Thought step
        thought = await self._think(input, context, history, system_prompt)

        # Action step
        action_result = await self._act(thought, input, context)

        # Observation step
        observation = self._observe(action_result)

        # Reflection step
        reflection = await self._reflect(thought, action_result, observation)

        # Store to short-term memory
        self.memory.store_short_term(
            agent=self.role,
            entry={"input": input, "output": reflection}
        )

        return {
            "agent": self.role,
            "thought": thought,
            "action": action_result,
            "observation": observation,
            "reflection": reflection,
            "output": reflection.get("final_answer", ""),
        }

    # ── Abstract methods each agent must implement ────────────────────────────

    @abstractmethod
    def _build_system_prompt(self, rag_context: str) -> str:
        pass

    @abstractmethod
    async def _act(self, thought: dict, input: str, context: dict) -> dict:
        pass

    # ── Shared reasoning helpers ──────────────────────────────────────────────

    async def _think(
        self,
        input: str,
        context: dict,
        history: list,
        system_prompt: str,
    ) -> dict:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
Context so far: {context}

History: {history}

Task: {input}

Think step by step about:
1. What is being asked?
2. What do I know about this?
3. What actions should I take?
4. What tools do I need?

Respond as JSON: {{"reasoning": "...", "plan": "...", "tools_needed": []}}
"""),
        ]
        response = await self.llm.agenerate([messages])
        return self._parse_json(response.generations[0][0].text)

    def _observe(self, action_result: dict) -> dict:
        return {
            "success": "error" not in action_result,
            "summary": str(action_result)[:500],
            "data": action_result,
        }

    async def _reflect(self, thought: dict, action_result: dict, observation: dict) -> dict:
        messages = [
            SystemMessage(content=f"You are {self.role}. Reflect on the completed action."),
            HumanMessage(content=f"""
Thought: {thought}
Action result: {action_result}
Observation: {observation}

Reflect: Was the goal achieved? What is the final answer?
Respond as JSON: {{"reflection": "...", "final_answer": "...", "confidence": 0.0-1.0}}
"""),
        ]
        response = await self.llm.agenerate([messages])
        return self._parse_json(response.generations[0][0].text)

    def _parse_json(self, text: str) -> dict:
        import json, re
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception:
            pass
        return {"raw": text}
