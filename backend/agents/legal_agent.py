"""Legal Agent"""
from agents.base_agent import BaseAgent
from langchain_core.messages import HumanMessage, SystemMessage


class LegalAgent(BaseAgent):
    role = "legal"
    goal = "Analyse contracts, compliance issues, and legal risks"
    tools = ["rag_retriever", "web_search"]

    def _build_system_prompt(self, rag_context: str) -> str:
        return f"""You are the Legal Agent — an expert in contract law, compliance, GDPR, and IP.
Always note IANAL (not legal advice). Flag high-risk items prominently.
Context: {rag_context}"""

    async def _act(self, thought: dict, input: str, context: dict) -> dict:
        messages = [
            SystemMessage(content=self._build_system_prompt("")),
            HumanMessage(content=f"Analyse legal aspects of: {input}\n\nRespond as JSON: {{\"risks\": [], \"compliance_checklist\": [], \"recommendations\": \"...\", \"disclaimer\": \"Not legal advice\"}}"),
        ]
        response = await self.llm.agenerate([messages])
        return self._parse_json(response.generations[0][0].text)
