import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from validate_crm_event import validate

def test_valid_outcome():
    row = {"eventId":"E1","profileKey":"CRM-1","outcomeType":"purchase","occurredAt":"2026-11-24T08:00:00Z","source":"AJO"}
    assert validate(row) == []

def test_unsupported_outcome_rejected():
    row = {"eventId":"E2","profileKey":"CRM-1","outcomeType":"send-refund","occurredAt":"2026-11-24T08:00:00Z","source":"AJO"}
    assert "unsupported outcomeType" in validate(row)

def test_missing_profile_key_rejected():
    row = {"eventId":"E3","outcomeType":"purchase","occurredAt":"2026-11-24T08:00:00Z","source":"AJO"}
    assert "missing profileKey" in validate(row)
