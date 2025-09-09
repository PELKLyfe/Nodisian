import asyncio
from typing import Dict, Any
from mcp.utils.audit import audit_log

class UIAdapter:
    def __init__(self, mcp):
        self.mcp = mcp

    async def ask(self, patient_id: str, scope: str, question: str):
        audit_log("UI.Ask", {"patient_id": patient_id, "scope": scope, "q": question})
        # route via MCP command
        return await self.mcp.execute_command("Summarizer.Answer", {"scope": scope, "question": question}, patient_id=patient_id)
