"""File Tool"""
import aiofiles, os


class FileTool:
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")

    def __init__(self):
        os.makedirs(self.BASE_DIR, exist_ok=True)

    async def write(self, filename: str, content: str) -> str:
        path = os.path.join(self.BASE_DIR, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        async with aiofiles.open(path, "w") as f:
            await f.write(content)
        return path

    async def read(self, filename: str) -> str:
        path = os.path.join(self.BASE_DIR, filename)
        async with aiofiles.open(path, "r") as f:
            return await f.read()

    async def list_files(self, subdir: str = "") -> list:
        target = os.path.join(self.BASE_DIR, subdir)
        return os.listdir(target) if os.path.exists(target) else []
