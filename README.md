# Salesforce CRM & AI Lab

Hands-on learning repository for Salesforce Sales Cloud, Service Cloud, CRM data modelling, REST integrations, Data Cloud (also referred to as Data 360 in current Salesforce positioning) and governed Agentforce patterns.

> Learning blueprint only. Uses synthetic data and local simulations; it does not connect to a Salesforce org or invoke Agentforce actions.

## Business outcome
Create a clean CRM operating model, integrate customer and engagement signals from an external experience platform, and design AI-assisted sales/service workflows with explicit permissions and human review.

## Core workstreams
1. CRM data model: Lead, Contact, Account, Opportunity, Case, Task and Campaign Member.
2. Data stewardship: record ownership, deduplication, field-level authority, consent and lifecycle state.
3. Integration: authenticated REST API patterns, idempotency, retries, error handling and audit trail.
4. Data Cloud: identity resolution, unified individual, calculated insights and activation concepts (subject to licensed features).
5. Agentforce: topics/instructions, actions, grounding, access controls, guardrails and human handoff.
6. Closed loop: AJO journey outcome → integration service → Salesforce Task/record update → sales/service outcome → approved feedback to AEP.

## Repository map
- `docs/` — architecture, data model, integration and agent safety
- `contracts/` — platform-neutral CRM payloads
- `data/` — synthetic records
- `src/` — local validation and idempotency example
- `tests/` — deterministic checks
- `ROADMAP.md` — 8-week hands-on plan

## Run locally
```bash
python -m venv .venv
pip install -e .[dev]
pytest
python src/validate_crm_event.py data/crm-outcomes.jsonl
```

## Security
Use OAuth and least-privilege connected-app permissions in any real org. Never commit client secrets, refresh tokens, production data or personal customer data. Use synthetic records only. Human approval is required for consequential sales/service actions during the lab.

## Source material
Based on the user's Google Drive consolidated Adobe/AEP/AJO/Salesforce guide and MarTech 2030 architecture notes. Validate current product naming, availability and licensing in Salesforce Help and the target org.