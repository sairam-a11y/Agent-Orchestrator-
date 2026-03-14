"""
Tools
-----
Web Search · Code Executor · File Tool · API Tool
"""

# ── web_search.py ─────────────────────────────────────────────────────────────
import aiohttp
import os
from typing import List, Dict


class WebSearchTool:
    """Tavily / DuckDuckGo web search wrapper."""

    async def run(self, query: str, max_results: int = 5) -> List[Dict]:
        api_key = os.getenv("TAVILY_API_KEY")
        if api_key:
            return await self._tavily(query, max_results, api_key)
        return await self._ddg(query, max_results)

    async def _tavily(self, query: str, n: int, key: str) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.tavily.com/search",
                json={"api_key": key, "query": query, "max_results": n},
            ) as r:
                data = await r.json()
                return data.get("results", [])

    async def _ddg(self, query: str, n: int) -> list:
        # Fallback: return placeholder when no key set
        return [{"title": f"Result for '{query}'", "url": "#", "content": "No API key set"}]
