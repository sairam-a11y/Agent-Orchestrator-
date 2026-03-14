"""
Research Agent — searches the web and summarises knowledge.
"""
from agents.base_agent import BaseAgent
from tools.web_search import WebSearchTool
from langchain_core.messages import HumanMessage, SystemMessage


class ResearchAgent(BaseAgent):
    role = "research"
    goal = "Search the web and synthesise accurate, up-to-date knowledge"
    tools = ["web_search", "rag_retriever"]

    def _build_system_prompt(self, rag_context: str) -> str:
        return f"""You are the Research Agent. Use web search and the knowledge base
to gather accurate, relevant information. Cite sources. Be concise and factual.

RAG context:
{rag_context}
"""

    async def _act(self, thought: dict, input: str, context: dict) -> dict:
        search = WebSearchTool()
        results = await search.run(input)
        messages = [
            SystemMessage(content=self._build_system_prompt("")),
            HumanMessage(content=f"Synthesise these search results into a clear summary.\n\nQuery: {input}\n\nResults: {results}"),
        ]
        response = await self.llm.agenerate([messages])
        return {"summary": response.generations[0][0].text, "sources": results}
