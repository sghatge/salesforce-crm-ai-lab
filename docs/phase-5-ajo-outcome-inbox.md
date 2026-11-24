# Phase 5 — AJO outcome inbox and governed CRM follow-up

The Salesforce lab now includes an **AJO outcome inbox** tab and the shared contract files:
- `contracts/customer-lifecycle-event.json`
- `contracts/salesforce-followup-action.json`

The inbox shows a synthetic AJO journey outcome and a proposed Salesforce Task payload. The request carries the journey correlation ID and is constrained to `PENDING_HUMAN_APPROVAL` with `requiresHumanApproval: true`.

The approval control is demonstrative only: no Salesforce record is written. Production integration requires identity matching, idempotency, least-privilege permissions, approval evidence and controlled API execution.

The canonical end-to-end sequence is documented in the AEP repository: `docs/enterprise-lifecycle-integration.md`.
