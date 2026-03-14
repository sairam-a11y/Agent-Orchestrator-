"""
Platform Logger & Monitoring
"""
from datetime import datetime
from collections import deque
from typing import Any, Dict
import json


class PlatformLogger:
    MAX_LOGS = 500

    def __init__(self):
        self._logs: deque = deque(maxlen=self.MAX_LOGS)

    def log_event(self, event: str, data: Dict[str, Any] = {}) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "data": data,
        }
        self._logs.append(entry)
        print(f"[{entry['timestamp']}] {event} | {json.dumps(data)[:120]}")

    def recent_logs(self, n: int = 50):
        logs = list(self._logs)
        return logs[-n:]

    def logs_by_event(self, event_prefix: str):
        return [l for l in self._logs if l["event"].startswith(event_prefix)]
