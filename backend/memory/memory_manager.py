"""
Memory Manager
--------------
Short-term memory (in-process ring buffer per agent)
Long-term memory  (vector store via RAG pipeline)
"""

from collections import defaultdict, deque
from typing import List, Dict, Any
from rag.rag_pipeline import DocumentLoader, RAGRetriever


class MemoryManager:
    SHORT_TERM_SIZE = 20  # entries per agent

    def __init__(self):
        # Short-term: {agent_name: deque of entries}
        self._short_term: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=self.SHORT_TERM_SIZE)
        )
        self._loader = DocumentLoader()
        self._retriever = RAGRetriever()

    # ── Short-term ────────────────────────────────────────────────────────────

    def store_short_term(self, agent: str, entry: Dict[str, Any]) -> None:
        self._short_term[agent].append(entry)

    def get_short_term(self, agent: str, n: int = 5) -> List[Dict]:
        history = list(self._short_term[agent])
        return history[-n:] if len(history) >= n else history

    def clear_short_term(self, agent: str) -> None:
        self._short_term[agent].clear()

    # ── Long-term (vector DB) ─────────────────────────────────────────────────

    async def store_long_term(self, content: str, source: str = "agent_memory") -> str:
        return await self._loader.ingest(content, source=source)

    async def recall(self, query: str) -> str:
        return await self._retriever.retrieve(query)

    # ── Convenience ───────────────────────────────────────────────────────────

    def get_all_agents(self) -> List[str]:
        return list(self._short_term.keys())

    def get_stats(self) -> Dict[str, int]:
        return {
            agent: len(buf)
            for agent, buf in self._short_term.items()
        }
