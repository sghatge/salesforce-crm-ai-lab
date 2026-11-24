# Agentforce design and safety checklist

## Agent design
- Define one narrow business objective and permitted user personas.
- Ground answers in approved CRM records and knowledge sources.
- Declare topics, instructions and actions explicitly.
- Restrict actions to least-privilege permissions.
- Validate record ownership, sharing, field-level security and consent.
- Require human confirmation for consequential actions such as opportunity changes, customer commitments, refunds or outbound communication unless separately approved by policy.
- Log inputs, retrieved context, action proposals, approvals, execution result and correlation ID.
- Provide a clear handoff when confidence, data quality or policy conditions fail.

## Lab agent concept
Lead Follow-up Assistant: summarize a synthetic lead's recent interactions, suggest a next action and draft a Task. It must not send messages or change opportunity stages automatically.

## Evaluation cases
- Missing or conflicting CRM data.
- User lacks permission to a record.
- Duplicate event replay.
- Opted-out customer.
- Low-confidence or unsupported request.
- Prompt injection in untrusted notes/fields.
- Human rejects proposed action.

Agentforce capabilities, product names and license prerequisites must be checked in the target Salesforce org.