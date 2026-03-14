"""Debug Agent"""
from agents.base_agent import BaseAgent
from tools.code_executor import CodeExecutorTool
from langchain_core.messages import HumanMessage, SystemMessage


class DebugAgent(BaseAgent):
    role = "debug"
    goal = "Analyse code for bugs, security issues, and suggest fixes"
    tools = ["code_executor", "static_analyser"]

    def _build_system_prompt(self, rag_context: str) -> str:
        return f"""You are the Debug Agent — an expert at code review, debugging, and security analysis.
Find bugs, performance issues, and security vulnerabilities. Always provide fixed code.

Context: {rag_context}"""

    async def _act(self, thought: dict, input: str, context: dict) -> dict:
        code = context.get("developer_output", {}).get("output", input)
        executor = CodeExecutorTool()
        exec_result = await executor.run(code)
        messages = [
            SystemMessage(content=self._build_system_prompt("")),
            HumanMessage(content=f"Analyse this code for issues:\n\n{code}\n\nExecution result: {exec_result}\n\nRespond as JSON: {{\"issues\": [], \"fixes\": {{}}, \"security_notes\": \"...\", \"fixed_code\": \"...\"}}"),
        ]
        response = await self.llm.agenerate([messages])
        return self._parse_json(response.generations[0][0].text)
