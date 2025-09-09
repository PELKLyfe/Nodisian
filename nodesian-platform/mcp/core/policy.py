import json, os
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception:  # PyYAML optional
    yaml = None

class Policy:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.id = data.get("policy_id", "unknown")

    @staticmethod
    def load(path_yaml: str, fallback_json: str = None) -> "Policy":
        if yaml is not None and os.path.exists(path_yaml):
            with open(path_yaml, "r") as f:
                data = yaml.safe_load(f)
            return Policy(data)
        if fallback_json and os.path.exists(fallback_json):
            with open(fallback_json, "r") as f:
                data = json.load(f)
            return Policy(data)
        raise FileNotFoundError("Policy file not found and no loader available. Install pyyaml or provide JSON.")

    def get_automations(self) -> List[Dict[str, Any]]:
        return self.data.get("automations", [])

    def freshness_sla(self) -> Dict[str, Any]:
        return self.data.get("freshness_sla", {})

    def commands(self) -> Dict[str, Any]:
        return self.data.get("commands", {})

    def ui_policy(self) -> Dict[str, Any]:
        return self.data.get("ui_policy", {})
