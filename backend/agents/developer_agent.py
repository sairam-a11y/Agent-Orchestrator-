"""
Developer Agent — generates production-ready code and software architecture.
"""
from agents.base_agent import BaseAgent
from tools.code_executor import CodeExecutorTool
from tools.file_tool import FileTool
from langchain_core.messages import HumanMessage, SystemMessage


class DeveloperAgent(BaseAgent):
    role = "developer"
    goal = "Generate clean, modular, production-ready code and software architecture"
    tools = ["code_executor", "file_system", "api_tool"]

    def _build_system_prompt(self, rag_context: str) -> str:
        return f"""You are the Developer Agent — a senior full-stack engineer.
Write clean, well-commented, production-ready code. Follow best practices.
Always provide: code, explanation, and how to run it.

Technical context:
{rag_context}
"""

    async def _act(self, thought: dict, input: str, context: dict) -> dict:
        messages = [
            SystemMessage(content=self._build_system_prompt("")),
            HumanMessage(content=f"""
Task: {input}

Context: {context.get('research_output', {}).get('output', '')}

Generate:
1. Architecture overview
2. Complete code (language appropriate for task)
3. File structure
4. How to run

Respond as JSON: {{"architecture": "...", "code": {{}}, "run_instructions": "..."}}
"""),
        ]
        response = await self.llm.agenerate([messages])
        result = self._parse_json(response.generations[0][0].text)

        # Optionally save generated files
        file_tool = FileTool()
        for filename, content in result.get("code", {}).items():
            await file_tool.write(filename, content)

        return result
