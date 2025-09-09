import asyncio, time, hashlib, json
from typing import Any, Dict, Callable, Awaitable, Optional
from mcp.core.bus import EventBus
from mcp.core.policy import Policy

class MCP:
    def __init__(self, policy: Policy, bus: EventBus):
        self.policy = policy
        self.bus = bus
        self.command_handlers: Dict[str, Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]] = {}
        self.artifact_cache: Dict[str, Dict[str, Any]] = {}  # artifact_type -> {patient_id: {data..., ts}}

    def register_command(self, name: str, handler: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]):
        self.command_handlers[name] = handler

    async def emit(self, event_type: str, payload: Dict[str, Any]):
        payload = dict(payload)
        payload["event_type"] = event_type
        await self.bus.publish(event_type, payload)
        # Run automations
        for rule in self.policy.get_automations():
            if rule.get("on_event") != event_type:
                continue
            # Very simple condition evaluator: Python eval on locals (safe subset). Replace with JMESPath in prod.
            conditions = rule.get("conditions", [])
            ok = True
            for c in conditions:
                try:
                    # Build a minimal context
                    delta = payload.get("delta", {})
                    artifacts = payload.get("artifacts", {})
                    scope = payload.get("scope")
                    ok = ok and eval(c, {"__builtins__": {}}, {"delta": delta, "artifacts": artifacts, "scope": scope})
                except Exception:
                    ok = False
            if not ok:
                continue
            for step in rule.get("do", []):
                cmd = step.get("command")
                inputs_tmpl = step.get("with", {})
                # render simple templates {{key}}
                inputs = {}
                for k, v in inputs_tmpl.items():
                    if isinstance(v, str) and v.startswith("{{") and v.endswith("}}"):
                        key = v.strip("{} ")
                        inputs[k] = payload.get(key)
                    else:
                        inputs[k] = v
                await self.execute_command(cmd, inputs, payload.get("patient_id"))

    async def execute_command(self, command: str, inputs: Dict[str, Any], patient_id: Optional[str] = None) -> Dict[str, Any]:
        if command not in self.command_handlers:
            raise ValueError(f"No handler for command {command}")
        # naive idempotency / debounce hint
        key_fields = json.dumps(inputs, sort_keys=True)
        id_key = hashlib.sha256((command + ":" + str(patient_id) + ":" + key_fields).encode()).hexdigest()[:16]
        # Execute
        res = await self.command_handlers[command](dict(inputs, correlation_id=id_key, patient_id=patient_id))
        return res

    def cache_artifact(self, artifact_type: str, patient_id: str, data: Dict[str, Any]):
        self.artifact_cache.setdefault(artifact_type, {})[patient_id] = dict(data, __ts=time.time())

    def get_artifact(self, artifact_type: str, patient_id: str) -> Optional[Dict[str, Any]]:
        return self.artifact_cache.get(artifact_type, {}).get(patient_id)
