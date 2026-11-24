# Salesforce CRM data model and ownership

| Object | Purpose | Example relationships | Lab stewardship rule |
|---|---|---|---|
| Lead | Unqualified prospect | Converts to Account/Contact/Opportunity | Deduplicate before create; capture source |
| Contact | Known person | Related to Account | Salesforce is CRM system of record in the reference architecture |
| Account | Organisation/customer | Parent of Contacts and Opportunities | Govern hierarchy and ownership |
| Opportunity | Revenue pipeline | Related to Account and often Contact roles | Preserve stage history and closed outcome |
| Case | Service issue | Related to Contact/Account | Restrict sensitive fields and access |
| Task | Follow-up action | Related to Lead/Contact/Account/Opportunity | Idempotent creation and clear owner/due date |
| Campaign Member | Campaign response | Relates Campaign to Lead/Contact | Define response status and attribution policy |

## Reference ownership
Salesforce owns CRM records and sales/service outcomes. AEP owns the unified experience profile and behavioural context in the reference design. AJO owns journey execution and engagement history. Consent ownership must be explicitly agreed; the reference guide assumes Salesforce or a central consent service is authoritative, with consent propagated to AEP and checked before activation.