# Salesforce CRM Intelligence Lab — User Guide

## Purpose
A hands-on simulator for core Salesforce CRM and governed automation concepts. It uses synthetic records and makes no API calls to Salesforce.

## Modules
1. **Overview:** CRM lifecycle and high-level object flow.
2. **CRM Data Model:** sample Account, Contact, Lead, Opportunity, Case and Campaign tables with relationship descriptions.
3. **Customer 360:** synthetic contact, account, sales pipeline and service history in one view.
4. **Lead Management:** illustrative weighted score (55% engagement, 45% fit), threshold qualification, duplicate review and session-only lead creation.
5. **Flow Simulator:** select a record, trigger, field, comparison operator and proposed action; inspect the simulated result.
6. **Service & Cases:** inspect priority, age and illustrative SLA status.
7. **CRM Analytics:** pipeline and weighted pipeline by opportunity; campaign response and pipeline association.
8. **Governance & AI:** checklist plus consent and human-approval policy gate for a proposed action.
9. **AJO Integration:** preview/download an AJO outcome event and Salesforce Task proposal.

## Local execution
```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Key rules demonstrated
- Keep an authoritative system of record for each field.
- Deduplicate before lead conversion or downstream CRM actions.
- Respect email opt-out and explicit SMS consent.
- Use least-privilege integration permissions.
- Require human review for consequential AI-proposed actions.
- Use correlation and idempotency identifiers for closed-loop integrations.
- Capture audit evidence and rejection reasons.

## Limitations
This is not Salesforce, Data Cloud or Agentforce. The data model is simplified; no org metadata is queried. Lead scoring, SLA targets, campaign attribution and Flow execution are illustrative. Session-created Leads are not persisted. No outbound messages or CRM writes occur.

## Next learning exercises
- Change the MQL threshold and inspect qualification changes.
- Add a duplicate Lead and observe the review gate.
- Configure a Flow condition on engagement or Case age.
- Inspect cases approaching SLA breach.
- Compare weighted pipeline across opportunity stages.
- Try an AI-proposed email for a contact who has opted out; confirm policy blocks it.
- Export an AJO outcome event and inspect the proposed Salesforce Task payload.
