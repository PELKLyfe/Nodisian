import asyncio, time
from typing import Dict, Any
from mcp.utils.audit import audit_log

class ScribeAgent:
    def __init__(self, mcp):
        self.mcp = mcp

    async def capture(self, req: Dict[str, Any]) -> Dict[str, Any]:
        patient_id = req.get("patient_id","unknown")
        await asyncio.sleep(0.05)
        note_id = f"note://draft/{patient_id}/{int(time.time())}"
        audit_log("Note.Drafted", {"patient_id": patient_id, "note_id": note_id})
        await self.mcp.emit("Note.Drafted", {"patient_id": patient_id, "note_id": note_id})
        return {"status": "OK", "note_id": note_id}
