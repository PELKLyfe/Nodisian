import asyncio
from collections import defaultdict
from typing import Callable, Dict, Any, List

class EventBus:
    def __init__(self):
        self._subs: Dict[str, List[Callable[[Dict[str, Any]], None]]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def publish(self, topic: str, event: Dict[str, Any]):
        # fan out to subscribers; don't block publisher on slow consumers
        async with self._lock:
            subs = list(self._subs.get(topic, []))
        for cb in subs:
            asyncio.create_task(cb(event))

    async def subscribe(self, topic: str, callback: Callable[[Dict[str, Any]], None]):
        async with self._lock:
            self._subs[topic].append(callback)

    async def topics(self):
        async with self._lock:
            return list(self._subs.keys())
