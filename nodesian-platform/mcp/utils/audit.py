import time
from typing import Dict, Any

def audit_log(event: str, payload: Dict[str, Any]):
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print(f"[AUDIT {ts}] {event} :: {payload}")
