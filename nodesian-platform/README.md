# Nodesian Platform (MCP + Agents)

This repo contains a production-oriented scaffold for the Nodesian platform:
- **MCP (Model Context Protocol) Orchestrator** with policy-driven automation, capabilities, audit, and event bus.
- **Agents**: Ingestion/Synthesis, DAG, MRF, GNN, Scribe, Summarizer, plus a UI Adapter shim.
- **Policy**: `nodesian-governance-v3.1-hardened.yaml` with non-sequential triggers, SLAs, debouncing, RACI, provenance.
- **Runner**: An end-to-end asyncio simulation to validate wiring and selective recomputes.

## Quick Start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install pyyaml
python runner.py
```

If `pyyaml` is not installed, the runner will load a JSON variant of the policy located at `config/policies/policy.json`.

## Layout

- `mcp/` – orchestrator, policy engine, bus, audit, security
- `agents/` – agent implementations
- `services/` – shared terminology, provenance, feature store (lightweight stubs)
- `config/policies/` – governance policies (YAML + JSON fallback)
- `runner.py` – creates an MCP instance, registers agents, simulates flows

## Notes

- This scaffold uses an in-memory event bus for simplicity. Swap `mcp/core/bus.py` with your Kafka/NATS adapter in prod.
- Command/RPC is implemented as MCP-dispatched async calls. You can replace with gRPC using `proto/` as a starting point.
- All artifacts carry minimal provenance and `correlation_id`. Extend as needed.
