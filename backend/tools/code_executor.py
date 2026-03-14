"""
Code Executor Tool
------------------
Runs Python code in a sandboxed subprocess with timeout.
"""
import asyncio
import sys
import tempfile
import os
from typing import Dict


class CodeExecutorTool:
    TIMEOUT = 15  # seconds

    async def run(self, code: str, language: str = "python") -> Dict:
        if language != "python":
            return {"output": "", "error": f"Language '{language}' not yet supported", "exit_code": 1}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f:
            f.write(code)
            tmp_path = f.name

        try:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, tmp_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=self.TIMEOUT
            )
            return {
                "output": stdout.decode()[:4000],
                "error": stderr.decode()[:2000],
                "exit_code": proc.returncode,
            }
        except asyncio.TimeoutError:
            proc.kill()
            return {"output": "", "error": "Execution timed out", "exit_code": -1}
        finally:
            os.unlink(tmp_path)
