import asyncio, time
from typing import Dict, Any
from mcp.utils.audit import audit_log

class DAGAgent:
    def __init__(self, mcp):
        self.mcp = mcp

    async def build(self, req: Dict[str, Any]) -> Dict[str, Any]:
        patient_id = req.get("patient_id")
        await asyncio.sleep(0.05)
        dag_pointer = f"dag://{patient_id}/{int(time.time())}"
        self.mcp.cache_artifact("DAG", patient_id, {"pointer": dag_pointer})
        audit_log("DAG.Updated", {"patient_id": patient_id, "dag_pointer": dag_pointer})
        await self.mcp.emit("DAG.Updated", {"patient_id": patient_id, "dag_pointer": dag_pointer, "pkg_pointer": req.get("pkg_pointer")})
        return {"status": "OK", "dag_pointer": dag_pointer}
