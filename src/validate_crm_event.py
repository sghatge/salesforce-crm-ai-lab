"""Validate synthetic engagement outcomes before CRM processing."""
import json
import sys
from datetime import datetime
from pathlib import Path

ALLOWED = {"journey_entered", "message_clicked", "purchase", "cart_recovered", "consent_withdrawn"}
SOURCES = {"AJO", "AEP", "WEB", "COMMERCE"}

def validate(row: dict) -> list[str]:
    errors = []
    for key in ("eventId", "profileKey", "outcomeType", "occurredAt", "source"):
        if not row.get(key): errors.append(f"missing {key}")
    if row.get("outcomeType") not in ALLOWED: errors.append("unsupported outcomeType")
    if row.get("source") not in SOURCES: errors.append("unsupported source")
    if row.get("occurredAt"):
        try: datetime.fromisoformat(row["occurredAt"].replace("Z", "+00:00"))
        except ValueError: errors.append("occurredAt must be ISO-8601")
    return errors

def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/crm-outcomes.jsonl")
    failures = 0
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip(): continue
        try: errors = validate(json.loads(line))
        except json.JSONDecodeError as exc: errors = [f"invalid JSON: {exc}"]
        print(("PASS" if not errors else "FAIL") + f" line {n}: " + ("valid" if not errors else "; ".join(errors)))
        failures += bool(errors)
    return 1 if failures else 0

if __name__ == "__main__": raise SystemExit(main())