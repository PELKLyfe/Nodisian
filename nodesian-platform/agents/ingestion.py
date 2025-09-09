import asyncio, time
from typing import Dict, Any
from mcp.utils.audit import audit_log

class IngestionAgent:
    def __init__(self, mcp):
        self.mcp = mcp

    async def ingest(self, req: Dict[str, Any]) -> Dict[str, Any]:
        patient_id = req.get("patient_id","unknown")
        await asyncio.sleep(0.05)
        delta = {"kind": req.get("kind","value_update"), "affects_distribution": req.get("affects_distribution", False)}
        pkg_pointer = f"pkg://{patient_id}/v{int(time.time())}"
        audit_log("PKG.Updated", {"patient_id": patient_id, "delta": delta, "pkg_pointer": pkg_pointer})
        await self.mcp.emit("PKG.Updated", {"patient_id": patient_id, "delta": delta, "pkg_pointer": pkg_pointer, "artifacts": {"DAG":{"stale":True},"MRF":{"stale":True},"Risk":{"stale":True}}})
        return {"status": "OK", "pkg_pointer": pkg_pointer}
