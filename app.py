import pandas as pd
import streamlit as st
st.set_page_config(page_title="Salesforce CRM and Agentforce Lab",page_icon="☁️",layout="wide")
st.title("☁️ Salesforce CRM | Data & Agentforce Governance Lab")
st.caption("CRM system of record · field ownership · lead qualification · governed agent actions")
st.info("Synthetic CRM workbench. No Salesforce org is connected and no records or tasks are written.")
seed=[
{"record_id":"L-2001","name":"Aarav Mehta","type":"Lead","source":"Web","score":72,"status":"Working","email_opt_out":False,"sms_opt_in":True,"owner":"Inside Sales"},
{"record_id":"L-2002","name":"Diya Shah","type":"Lead","source":"Webinar","score":48,"status":"New","email_opt_out":True,"sms_opt_in":True,"owner":"Unassigned"},
{"record_id":"C-3001","name":"Kabir Rao","type":"Contact","source":"Existing customer","score":88,"status":"Qualified","email_opt_out":False,"sms_opt_in":False,"owner":"Enterprise Sales"},
{"record_id":"L-2003","name":"Mira Iyer","type":"Lead","source":"Partner","score":61,"status":"Working","email_opt_out":False,"sms_opt_in":True,"owner":"Inside Sales"}]
if "crm" not in st.session_state: st.session_state.crm=pd.DataFrame(seed)
a,b,c=st.columns(3); a.metric("CRM records",len(st.session_state.crm)); b.metric("Leads",int((st.session_state.crm.type=="Lead").sum())); c.metric("Contacts",int((st.session_state.crm.type=="Contact").sum()))
t1,t2,t3,t4=st.tabs(["CRM explorer","Lead qualification","Agent action gate","Field ownership"])
with t1:
 st.dataframe(st.session_state.crm,use_container_width=True,hide_index=True)
 with st.expander("Create a synthetic lead"):
  name=st.text_input("Full name"); source=st.selectbox("Lead source",["Web","Webinar","Partner","Event","Referral"]); score=st.slider("Engagement score",0,100,35); optout=st.checkbox("Has opted out of email")
  if st.button("Add lead"):
   if not name.strip(): st.error("Enter a name.")
   else:
    n={"record_id":f"L-{2004+len(st.session_state.crm)}","name":name.strip(),"type":"Lead","source":source,"score":score,"status":"New","email_opt_out":optout,"sms_opt_in":False,"owner":"Unassigned"}
    st.session_state.crm=pd.concat([st.session_state.crm,pd.DataFrame([n])],ignore_index=True); st.success("Synthetic lead created in this session.")
with t2:
 threshold=st.slider("Illustrative MQL threshold",30,100,65)
 eligible=st.session_state.crm[(st.session_state.crm.type=="Lead")&(st.session_state.crm.score>=threshold)]
 st.metric("Leads meeting threshold",len(eligible)); st.dataframe(eligible[["record_id","name","source","score","status","owner"]],use_container_width=True,hide_index=True)
 if st.button("Simulate MQL handoff"):
  if eligible.empty: st.warning("No leads meet this threshold.")
  else: st.success(f"{len(eligible)} lead(s) qualify for simulated handoff. Production flow must deduplicate against Contact, validate fields, create Task and preserve attribution.")
with t3:
 rec=st.selectbox("CRM record",st.session_state.crm.to_dict("records"),format_func=lambda x:f"{x['name']} · {x['record_id']}")
 action=st.selectbox("Proposed agent action",["Draft follow-up email","Create sales task","Send SMS","Update lead status","Summarize support case"])
 channel="Email" if action=="Draft follow-up email" else "SMS" if action=="Send SMS" else None
 rationale=st.text_area("Agent rationale","High engagement and recent activity indicate timely sales follow-up.")
 checks=[]
 if channel=="Email": checks.append(("Email consent",not rec["email_opt_out"],"HasOptedOutOfEmail must be false"))
 if channel=="SMS": checks.append(("SMS consent",rec["sms_opt_in"],"Explicit SMS opt-in required"))
 checks += [("Stable record identity",bool(rec["record_id"]),"CRM record ID required"),("Human review",True,"Customer-impacting actions require approval")]
 for label,ok,why in checks: st.write(("✅" if ok else "⛔"),label,"—",why)
 if st.button("Evaluate proposed action",type="primary"):
  if all(x[1] for x in checks):
   st.success("POLICY PASS — prepare for human approval. Nothing is executed.")
   st.json({"record_id":rec["record_id"],"action":action,"status":"PENDING_HUMAN_APPROVAL","rationale":rationale})
  else:
   st.error("POLICY REJECT — consent or identity requirement failed.")
   st.json({"record_id":rec["record_id"],"action":action,"status":"REJECTED","violations":[x[0] for x in checks if not x[1]]})
 st.caption("Agentforce needs trusted grounding, least privilege, explicit consent and auditable human approval boundaries.")
with t4:
 matrix=pd.DataFrame([
 ["Account / Contact / Lead","Salesforce","Salesforce → AEP","CRM identity and attributes"],
 ["Opportunity / Case / Task","Salesforce","Salesforce → AEP when useful","Sales and service outcomes"],
 ["Consent preference","Salesforce (per org policy)","Salesforce → AEP/AJO","Enforce before activation"],
 ["Web / app event","AEP","Sources → AEP","Behavioral context"],
 ["Unified profile / identity graph","AEP","AEP profile services","Identity resolution"],
 ["Journey / offer decision","AJO","AEP profile → AJO","Experience orchestration"],
 ["Journey outcome","AEP dataset; CRM summary","AJO/AEP → Salesforce","Closed-loop action"]],columns=["Data domain","System of record","Typical flow","Reason"])
 st.dataframe(matrix,use_container_width=True,hide_index=True)
 st.warning("Avoid competing owners for the same field. Define authoritative source, sync direction, conflict rule and steward.")
with st.expander("Closed-loop integration pattern"):
 st.markdown("1. Salesforce Lead/Contact/Consent syncs to AEP.\n2. AEP resolves CRM ID, email and ECID and enriches profiles with behavioral events.\n3. AJO evaluates event, audience, consent and fatigue before a journey action.\n4. Outcomes return through AEP and an approved integration to Salesforce Task, Opportunity, Case or Campaign Member.\n5. A policy gate validates agent proposals and records approvals, rejections and audit evidence.")
st.caption("Source alignment: Consolidated Adobe/AEP/AJO/Salesforce Guide and MarTech 2030 Governed AI Agent Architecture. Synthetic records only.")
