import asyncio, os, json
from mcp.core.bus import EventBus
from mcp.core.policy import Policy
from mcp.core.engine import MCP
from agents.ingestion import IngestionAgent
from agents.dag import DAGAgent
from agents.mrf import MRFAgent
from agents.gnn import GNNAgent
from agents.scribe import ScribeAgent
from agents.summarizer import SummarizerAgent

POLICY_YAML = "config/policies/nodesian-governance-v3.1-hardened.yaml"
POLICY_JSON = "config/policies/policy.json"

async def main():
    bus = EventBus()
    policy = Policy.load(POLICY_YAML, POLICY_JSON)
    mcp = MCP(policy, bus)

    # Instantiate agents
    ingestion = IngestionAgent(mcp)
    dag = DAGAgent(mcp)
    mrf = MRFAgent(mcp)
    gnn = GNNAgent(mcp)
    scribe = ScribeAgent(mcp)
    summarizer = SummarizerAgent(mcp)

    # Register commands
    mcp.register_command("Ingestion.Ingest", ingestion.ingest)
    mcp.register_command("DAG.Build", dag.build)
    mcp.register_command("MRF.Fit", mrf.fit)
    mcp.register_command("GNN.ScoreRisk", gnn.score)
    mcp.register_command("Summarizer.ComposeTiles", summarizer.compose_tiles)

    # Minimal placeholder for Summarizer.Answer so UIAdapter could call it
    async def answer(req):
        return {"status":"OK","answer":"stubbed","patient_id": req.get("patient_id")}
    mcp.register_command("Summarizer.Answer", answer)

    # Simulate flows
    patient_id = "P123"
    # 1) Ingest a temporal boundary change → triggers DAG.Build (if stale)
    await mcp.execute_command("Ingestion.Ingest", {"kind":"temporal_boundary"}, patient_id=patient_id)
    # 2) Ingest distribution shift → triggers MRF.Fit → triggers GNN.ScoreRisk → tiles preview
    await mcp.execute_command("Ingestion.Ingest", {"kind":"value_update", "affects_distribution": True}, patient_id=patient_id)
    # 3) Promote risk manually (simulate provider approval)
    await mcp.emit("Risk.Promoted", {"patient_id": patient_id, "risk_pointer": "risk://simulate/latest"})

    print("\\nArtifacts cache snapshot:")
    print(json.dumps(mcp.artifact_cache, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
