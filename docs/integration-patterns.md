# Integration patterns: AEP/AJO ↔ Salesforce

## Pattern A — Salesforce to AEP
Synchronize approved Lead/Contact attributes and consent to AEP through supported source/connector or integration patterns. Map Salesforce Contact ID to a CRM identity namespace. Keep source ownership and field-level mappings explicit.

## Pattern B — AJO outcome to Salesforce
AJO outcome/event becomes an approved integration message. Middleware validates schema, consent context, idempotency key and action policy. Salesforce creates/updates an appropriate Task, Campaign Member or other approved record. Avoid creating an Opportunity automatically without business rules and human review.

## Pattern C — Salesforce outcome back to AEP
Closed Won/Lost, case resolution or updated consent may be synchronized to AEP to improve future segmentation and journey suppression. Define latency, deletion, correction and replay behaviour.

## Reliability requirements
- OAuth-based authentication and least privilege.
- Idempotency key per business event/action.
- Retry transient errors with bounded exponential backoff.
- Dead-letter handling for permanent failures.
- Correlation ID and audit record.
- Schema versioning and contract tests.
- No secrets in source control.

These are architecture patterns, not tenant-specific connector setup instructions.