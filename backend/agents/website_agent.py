"""Website Agent"""
from agents.base_agent import BaseAgent
from tools.file_tool import FileTool
from langchain_core.messages import HumanMessage, SystemMessage


class WebsiteAgent(BaseAgent):
    role = "website"
    goal = "Create landing pages, UI components, and web content"
    tools = ["file_system", "web_search"]

    def _build_system_prompt(self, rag_context: str) -> str:
        return f"""You are the Website Agent — a senior UI/UX engineer and copywriter.
Generate beautiful, responsive HTML/CSS/JS for landing pages and UI components.
Context: {rag_context}"""

    async def _act(self, thought: dict, input: str, context: dict) -> dict:
        messages = [
            SystemMessage(content=self._build_system_prompt("")),
            HumanMessage(content=f"""
Create a landing page / UI for: {input}

Context: {context.get('research_output', {}).get('output', '')}

Respond as JSON: {{
  "html": "...",
  "sections": ["hero", "features", "pricing", "cta"],
  "copy_notes": "..."
}}
"""),
        ]
        response = await self.llm.agenerate([messages])
        result = self._parse_json(response.generations[0][0].text)
        
        # Save generated website
        if "html" in result:
            file_tool = FileTool()
            await file_tool.write("index.html", result["html"])
            
        return result
