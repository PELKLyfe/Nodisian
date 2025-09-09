import asyncio, time
from typing import Dict, Any
from mcp.utils.audit import audit_log

class SummarizerAgent:
    def __init__(self, mcp):
        self.mcp = mcp

    async def compose_tiles(self, req: Dict[str, Any]) -> Dict[str, Any]:
        patient_id = req.get("patient_id")
        mode = req.get("mode", "preview")
        risk_pointer = req.get("risk_pointer")
        await asyncio.sleep(0.03)
        tile_id = f"tile://{patient_id}/{mode}/{int(time.time())}"
        payload = {"patient_id": patient_id, "risk_pointer": risk_pointer, "tile_id": tile_id, "mode": mode}
        audit_log("Note.TilesReady", payload)
        await self.mcp.emit("Note.TilesReady", payload)
        return {"status": "OK", "tile_id": tile_id, "mode": mode}
