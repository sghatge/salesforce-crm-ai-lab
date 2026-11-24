import json
from datetime import datetime, timezone
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Salesforce CRM Intelligence Lab", page_icon="☁️", layout="wide")
st.title("☁️ Salesforce CRM Intelligence Lab")
st.caption("Explore customer data • qualify leads • simulate Flow automation • govern AI-assisted actions • measure outcomes")
st.info("Educational simulator using synthetic data only. No Salesforce org, Data Cloud or Agentforce tenant is connected. No CRM records are written and no messages are sent.")

ACCOUNTS = [
    {"account_id":"A-1001","account_name":"Northstar Retail","industry":"Retail","region":"West","annual_revenue":85000000,"segment":"Enterprise"},
    {"account_id":"A-1002","account_name":"BluePeak Finance","industry":"Financial Services","region":"South","annual_revenue":42000000,"segment":"Mid-Market"},
    {"account_id":"A-1003","account_name":"GreenLeaf Health","industry":"Healthcare","region":"West","annual_revenue":26000000,"segment":"Mid-Market"},
    {"account_id":"A-1004","account_name":"Orbit Technologies","industry":"Technology","region":"North","annual_revenue":120000000,"segment":"Enterprise"},
]
CONTACTS = [
    {"contact_id":"C-3001","name":"Kabir Rao","account_id":"A-1001","email":"kabir@example.test","email_opt_out":False,"sms_opt_in":False,"lifecycle":"Customer"},
    {"contact_id":"C-3002","name":"Mira Iyer","account_id":"A-1002","email":"mira@example.test","email_opt_out":False,"sms_opt_in":True,"lifecycle":"Prospect"},
    {"contact_id":"C-3003","name":"Tara Desai","account_id":"A-1004","email":"tara@example.test","email_opt_out":True,"sms_opt_in":True,"lifecycle":"Customer"},
]
LEADS = [
    {"lead_id":"L-2001","name":"Aarav Mehta","company":"Northstar Retail","source":"Web","engagement":82,"fit":88,"status":"Working","owner":"Inside Sales","email_opt_out":False,"duplicate":False},
    {"lead_id":"L-2002","name":"Diya Shah","company":"BluePeak Finance","source":"Webinar","engagement":45,"fit":72,"status":"New","owner":"Unassigned","email_opt_out":True,"duplicate":False},
    {"lead_id":"L-2003","name":"Neel Kapoor","company":"Orbit Technologies","source":"Partner","engagement":68,"fit":95,"status":"New","owner":"Unassigned","email_opt_out":False,"duplicate":False},
    {"lead_id":"L-2004","name":"Mira Iyer","company":"GreenLeaf Health","source":"Event","engagement":61,"fit":60,"status":"Working","owner":"Inside Sales","email_opt_out":False,"duplicate":True},
    {"lead_id":"L-2005","name":"Rohan Sen","company":"Northstar Retail","source":"Referral","engagement":91,"fit":80,"status":"Qualified","owner":"Enterprise Sales","email_opt_out":False,"duplicate":False},
]
OPPORTUNITIES = [
    {"opportunity_id":"O-4001","account":"Northstar Retail","stage":"Proposal","amount":1250000,"probability":65,"owner":"Enterprise Sales","days_open":34},
    {"opportunity_id":"O-4002","account":"BluePeak Finance","stage":"Qualification","amount":480000,"probability":25,"owner":"Inside Sales","days_open":12},
    {"opportunity_id":"O-4003","account":"Orbit Technologies","stage":"Negotiation","amount":2400000,"probability":80,"owner":"Enterprise Sales","days_open":58},
    {"opportunity_id":"O-4004","account":"GreenLeaf Health","stage":"Discovery","amount":720000,"probability":15,"owner":"Inside Sales","days_open":21},
]
CASES = [
    {"case_id":"CS-5001","contact":"Kabir Rao","subject":"Order status not updated","priority":"High","status":"New","age_hours":19,"sla_hours":24,"channel":"Web"},
    {"case_id":"CS-5002","contact":"Mira Iyer","subject":"Invoice clarification","priority":"Medium","status":"Working","age_hours":31,"sla_hours":48,"channel":"Email"},
    {"case_id":"CS-5003","contact":"Tara Desai","subject":"Access issue","priority":"Critical","status":"New","age_hours":7,"sla_hours":8,"channel":"Phone"},
    {"case_id":"CS-5004","contact":"Kabir Rao","subject":"Product feedback","priority":"Low","status":"Closed","age_hours":52,"sla_hours":72,"channel":"Web"},
]
CAMPAIGNS = [
    {"campaign_id":"CMP-01","campaign":"Q4 Product Webinar","members":420,"responded":96,"influenced_pipeline":1850000,"status":"Completed"},
    {"campaign_id":"CMP-02","campaign":"Retail Upgrade Program","members":310,"responded":84,"influenced_pipeline":2650000,"status":"Active"},
    {"campaign_id":"CMP-03","campaign":"Customer Advocacy","members":180,"responded":72,"influenced_pipeline":940000,"status":"Completed"},
]

def score_lead(engagement, fit):
    return round(0.55 * engagement + 0.45 * fit)

def qualify_lead(row, threshold, duplicate_policy=True):
    score = score_lead(row["engagement"], row["fit"])
    reasons = []
    if score < threshold: reasons.append("Below qualification score")
    if duplicate_policy and row["duplicate"]: reasons.append("Potential duplicate requires review")
    return score, not reasons, reasons

def evaluate_flow(record, trigger, condition_field, operator, threshold, action):
    value = record.get(condition_field)
    try:
        left, right = float(value), float(threshold)
        passed = {"greater than": left > right, "greater than or equal": left >= right, "less than": left < right, "equal to": left == right}.get(operator, False)
    except (TypeError, ValueError):
        passed = str(value).lower() == str(threshold).lower() if operator == "equal to" else False
    return {"trigger":trigger,"record_id":record.get("lead_id") or record.get("contact_id") or record.get("case_id"),"condition":f"{condition_field} {operator} {threshold}","actual_value":value,"result":"PASS" if passed else "NO MATCH","proposed_action":action if passed else "No action","execution":"SIMULATED — no Salesforce write"}

def case_sla_status(row):
    if row["status"] == "Closed": return "Closed"
    ratio = row["age_hours"] / max(row["sla_hours"], 1)
    return "Breached" if ratio >= 1 else "At risk" if ratio >= .75 else "Within SLA"

if "leads" not in st.session_state:
    st.session_state.leads = pd.DataFrame(LEADS)
if "flow_history" not in st.session_state:
    st.session_state.flow_history = []

accounts = pd.DataFrame(ACCOUNTS)
contacts = pd.DataFrame(CONTACTS)
leads = st.session_state.leads.copy()
opps = pd.DataFrame(OPPORTUNITIES)
cases = pd.DataFrame(CASES)
campaigns = pd.DataFrame(CAMPAIGNS)

tabs = st.tabs(["Overview","CRM Data Model","Customer 360","Lead Management","Flow Simulator","Service & Cases","CRM Analytics","Governance & AI","AJO Integration"])

with tabs[0]:
    st.subheader("Salesforce CRM operating model")
    a,b,c,d = st.columns(4)
    a.metric("Accounts",len(accounts)); b.metric("Leads",len(leads)); c.metric("Opportunities",len(opps)); d.metric("Open cases",int((cases.status!="Closed").sum()))
    st.graphviz_chart("""
    digraph crm {
      rankdir=LR; graph [bgcolor="transparent"]; node [shape=box,style="rounded,filled",fontname="Arial",color="#64748b",fillcolor="#eaf2ff"];
      lead [label="Lead capture"]; qualify [label="Score + deduplicate"]; convert [label="Account + Contact"]; opp [label="Opportunity"]; close [label="Closed won / lost"];
      service [label="Case + service"]; feedback [label="Customer outcomes"]; lead->qualify->convert->opp->close; convert->service->feedback; close->feedback;
    }
    """)
    st.markdown("**CRM lifecycle:** capture → qualify → convert → manage opportunity → serve customer → measure outcomes.")
    st.caption("This is a conceptual CRM process map, not an actual Salesforce org schema or automation.")

with tabs[1]:
    st.subheader("Object and relationship explorer")
    object_name = st.selectbox("Select a CRM object",["Account","Contact","Lead","Opportunity","Case","Campaign"])
    frames = {"Account":accounts,"Contact":contacts,"Lead":leads,"Opportunity":opps,"Case":cases,"Campaign":campaigns}
    st.dataframe(frames[object_name],use_container_width=True,hide_index=True)
    relations = pd.DataFrame([
        ["Account","Contact","One-to-many","Contacts belong to an Account"],
        ["Account","Opportunity","One-to-many","Commercial pipeline against an Account"],
        ["Lead","Account / Contact","Conversion relationship","Qualified Lead may be converted"],
        ["Contact","Case","One-to-many","Service history associated with a person"],
        ["Campaign","Campaign Member","One-to-many","Tracks Lead/Contact campaign membership"],
        ["Opportunity","Campaign","Influence relationship","Campaign influence attribution"],
    ],columns=["Parent / object","Related object","Relationship","Business meaning"])
    st.markdown("**Relationship map**")
    st.dataframe(relations,use_container_width=True,hide_index=True)
    st.info("The lab uses simplified synthetic tables. Salesforce standard objects, lookup/master-detail relationships and org customizations may differ.")

with tabs[2]:
    st.subheader("Unified customer view")
    customer = st.selectbox("Choose a customer",contacts.contact_id.tolist(),format_func=lambda x: contacts.loc[contacts.contact_id==x,"name"].iloc[0])
    person = contacts.loc[contacts.contact_id==customer].iloc[0].to_dict()
    acct = next((x for x in ACCOUNTS if x["account_id"]==person["account_id"]),{})
    related_cases = cases[cases.contact==person["name"]]
    related_opps = opps[opps.account==acct.get("account_name")]
    x,y,z = st.columns(3)
    x.metric("Lifecycle",person["lifecycle"]); y.metric("Open cases",int((related_cases.status!="Closed").sum())); z.metric("Opportunities",len(related_opps))
    st.markdown("**Identity and contact**"); st.json({k:person[k] for k in ["contact_id","name","email","email_opt_out","sms_opt_in","lifecycle"]})
    st.markdown("**Account context**"); st.json(acct)
    st.markdown("**Service history**"); st.dataframe(related_cases,use_container_width=True,hide_index=True)
    st.markdown("**Sales pipeline**"); st.dataframe(related_opps,use_container_width=True,hide_index=True)
    st.caption("Illustrative 360-degree view assembled from local synthetic records. No cross-system identity graph is queried.")

with tabs[3]:
    st.subheader("Lead scoring, qualification and assignment")
    threshold = st.slider("MQL qualification threshold",30,100,65)
    owner_map = {"Enterprise":"Enterprise Sales","Mid-Market":"Inside Sales","SMB":"Digital Sales"}
    rows=[]
    for r in st.session_state.leads.to_dict("records"):
        score,qualified,reasons=qualify_lead(r,threshold)
        rows.append({**r,"score":score,"qualification":"Qualified" if qualified else "Review / nurture","reason":"; ".join(reasons) if reasons else "Meets score and duplicate checks"})
    scored = pd.DataFrame(rows)
    st.metric("Qualified leads",int((scored.qualification=="Qualified").sum()))
    st.dataframe(scored[["lead_id","name","company","source","engagement","fit","score","qualification","owner","reason"]],use_container_width=True,hide_index=True)
    st.markdown("**Create synthetic lead**")
    with st.form("new_lead_form"):
        name=st.text_input("Name")
        company=st.text_input("Company")
        source=st.selectbox("Source",["Web","Webinar","Partner","Event","Referral"])
        engagement=st.slider("Engagement score",0,100,50)
        fit=st.slider("Fit score",0,100,60)
        duplicate=st.checkbox("Potential duplicate")
        submitted=st.form_submit_button("Add lead to this session")
    if submitted:
        if not name.strip() or not company.strip():
            st.error("Name and company are required.")
        else:
            new_id=f"L-{2001+len(st.session_state.leads)}"
            new={"lead_id":new_id,"name":name.strip(),"company":company.strip(),"source":source,"engagement":engagement,"fit":fit,"status":"New","owner":"Unassigned","email_opt_out":False,"duplicate":duplicate}
            st.session_state.leads=pd.concat([st.session_state.leads,pd.DataFrame([new])],ignore_index=True)
            st.success(f"Synthetic lead {new_id} added to this session. Refresh the tab to see updated scoring.")
    st.caption("Scoring weights and thresholds are lab assumptions. A production model requires calibration, fairness review and CRM governance.")

with tabs[4]:
    st.subheader("Salesforce Flow decision simulator")
    st.write("Configure a record-triggered Flow-style rule and evaluate it against one synthetic record.")
    object_type=st.selectbox("Record type",["Lead","Contact","Case"])
    source_records={"Lead":st.session_state.leads.to_dict("records"),"Contact":CONTACTS,"Case":CASES}
    rec=st.selectbox("Record",source_records[object_type],format_func=lambda x: f"{x.get('name') or x.get('contact') or x.get('subject')} · {x.get('lead_id') or x.get('contact_id') or x.get('case_id')}")
    trigger=st.selectbox("Trigger",["Record created","Record updated","Scheduled path"])
    field_options=list(rec.keys())
    field=st.selectbox("Condition field",field_options,index=field_options.index("engagement") if "engagement" in field_options else 0)
    operator=st.selectbox("Operator",["greater than","greater than or equal","less than","equal to"])
    default_value=str(rec[field]) if field in rec else "0"
    threshold_value=st.text_input("Compare value", "65" if field=="engagement" else default_value)
    action=st.selectbox("Proposed Flow action",["Assign owner","Create follow-up Task","Update lifecycle status","Create Case escalation","Send notification (simulation only)"])
    if st.button("Run Flow simulation",type="primary"):
        result=evaluate_flow(rec,trigger,field,operator,threshold_value,action)
        st.session_state.flow_history.append(result)
        st.json(result)
    if st.session_state.flow_history:
        st.markdown("**Recent simulation history**")
        st.dataframe(pd.DataFrame(st.session_state.flow_history[-10:]),use_container_width=True,hide_index=True)

with tabs[5]:
    st.subheader("Service Cloud case management")
    case_view=cases.copy()
    case_view["sla_status"]=case_view.apply(lambda r:case_sla_status(r.to_dict()),axis=1)
    st.dataframe(case_view,use_container_width=True,hide_index=True)
    a,b,c=st.columns(3)
    a.metric("SLA breached",int((case_view.sla_status=="Breached").sum()))
    b.metric("At risk",int((case_view.sla_status=="At risk").sum()))
    c.metric("Within SLA",int((case_view.sla_status=="Within SLA").sum()))
    case_id=st.selectbox("Inspect case",case_view.case_id.tolist())
    case=case_view[case_view.case_id==case_id].iloc[0].to_dict()
    st.json({"case_id":case["case_id"],"subject":case["subject"],"priority":case["priority"],"sla_status":case["sla_status"],"recommended_route":"Specialist queue" if case["priority"]=="Critical" else "Standard service queue"})
    st.caption("SLA thresholds and routing recommendations are illustrative. They are not contractual service commitments.")

with tabs[6]:
    st.subheader("CRM and campaign performance")
    weighted=opps.assign(weighted_value=opps.amount*opps.probability/100)
    a,b,c=st.columns(3)
    a.metric("Open pipeline",f"₹{opps.amount.sum():,.0f}")
    b.metric("Weighted pipeline",f"₹{weighted.weighted_value.sum():,.0f}")
    c.metric("Campaign members",int(campaigns.members.sum()))
    stage=opps.groupby("stage",as_index=False).agg(opportunities=("opportunity_id","count"),pipeline=("amount","sum"))
    st.markdown("**Opportunity pipeline by stage**"); st.bar_chart(stage.set_index("stage")["pipeline"])
    st.dataframe(weighted[["opportunity_id","account","stage","amount","probability","weighted_value","days_open"]],use_container_width=True,hide_index=True)
    camp=campaigns.copy()
    camp["response_rate_pct"]=(camp.responded/camp.members*100).round(1)
    st.markdown("**Campaign performance**"); st.dataframe(camp,use_container_width=True,hide_index=True)
    st.download_button("Export campaign analytics CSV",camp.to_csv(index=False).encode(),file_name="salesforce_campaign_analytics.csv",mime="text/csv")
    st.caption("Campaign influence is represented as sample pipeline association, not causal attribution or ROI proof.")

with tabs[7]:
    st.subheader("Data governance and AI action control")
    governance = [
        "Record identity and duplicate checks completed",
        "Field-level system of record and ownership documented",
        "Email opt-out and SMS consent checked before activation",
        "Least-privilege permissions defined for integrations",
        "Agent action grounded in approved CRM records",
        "Human approval required for consequential actions",
        "Idempotency key and retry behaviour defined",
        "Audit trail captures proposal, approver and outcome",
        "PII and secrets excluded from logs and source control",
        "Error and rollback path documented",
    ]
    completed=[st.checkbox(item,key="gov_"+str(i)) for i,item in enumerate(governance)]
    score=sum(completed)
    st.metric("Governance readiness",f"{score}/{len(governance)}",f"{score/len(governance):.0%} complete")
    st.progress(score/len(governance))
    st.markdown("**Agent action gate**")
    action_record=st.selectbox("Customer record",contacts.contact_id.tolist(),format_func=lambda x:contacts.loc[contacts.contact_id==x,"name"].iloc[0],key="agent_contact")
    target=contacts[contacts.contact_id==action_record].iloc[0].to_dict()
    proposed=st.selectbox("Proposed action",["Draft follow-up email","Send SMS","Create sales Task","Update customer lifecycle"])
    consent_ok=(not target["email_opt_out"]) if proposed=="Draft follow-up email" else target["sms_opt_in"] if proposed=="Send SMS" else True
    human=st.checkbox("Human reviewer has approved this proposed action")
    st.write("Consent check:", "PASS" if consent_ok else "BLOCK")
    st.write("Human approval:", "APPROVED" if human else "PENDING")
    if st.button("Evaluate AI action policy"):
        allowed=consent_ok and human
        st.json({"record_id":target["contact_id"],"proposed_action":proposed,"policy_result":"PASS_PENDING_EXECUTION" if allowed else "BLOCKED","consent_check":consent_ok,"human_approval":human,"executed":False})
        if allowed: st.success("Policy checks passed. This remains a proposal; no action was executed.")
        else: st.error("Action blocked. Resolve consent or approval requirement.")

with tabs[8]:
    st.subheader("AJO → Salesforce closed-loop outcome inbox")
    st.caption("Simulate an inbound journey outcome and prepare a reviewable CRM task proposal.")
    customer_id=st.selectbox("Customer CRM ID",contacts.contact_id.tolist())
    outcome=st.selectbox("Journey outcome",["message_delivered","message_clicked","message_blocked","purchase_converted","journey_exited"])
    reason=st.text_input("Outcome detail","Customer engaged with abandoned-cart reminder")
    corr=st.text_input("Correlation ID",f"CORR-{customer_id}-AJO-DEMO")
    payload={"eventId":f"SF-INBOX-{customer_id}-001","correlationId":corr,"occurredAt":datetime.now(timezone.utc).isoformat(),"source":"AJO_SIMULATOR","eventType":outcome,"customer":{"crmId":customer_id},"detail":reason,"synthetic":True}
    st.json(payload)
    task={"requestId":f"TASK-{corr}","correlationId":corr,"recordId":customer_id,"actionType":"CREATE_TASK","subject":"Review customer journey outcome","description":reason,"status":"PENDING_HUMAN_APPROVAL","requiresHumanApproval":True}
    st.markdown("**Proposed Salesforce Task — not executed**")
    st.json(task)
    st.download_button("Download outcome event JSON",json.dumps(payload,indent=2).encode(),file_name="ajo_to_salesforce_outcome.json",mime="application/json")
    st.download_button("Download task proposal JSON",json.dumps(task,indent=2).encode(),file_name="salesforce_task_proposal.json",mime="application/json")
    st.warning("This is a local contract preview. It does not call Salesforce REST APIs, create a Task or update a record.")

st.divider()
st.caption("Salesforce CRM Intelligence Lab • Synthetic data • Educational use • No live Salesforce or Agentforce connection")
