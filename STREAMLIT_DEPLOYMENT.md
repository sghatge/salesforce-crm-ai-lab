# Run and deploy this Streamlit demo

## Local run
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

## Streamlit Community Cloud
1. Sign in at https://share.streamlit.io/ with the GitHub account that owns this repository.
2. Select New app, choose this repository and the main branch.
3. Set the main file path to app.py.
4. Deploy. Do not add secrets or real customer data.
5. Add the generated app URL to the portfolio index after deployment.

## Scope and safety
- Fabricated sample records only.
- No Adobe or Salesforce tenant connection, outbound messages, credentials or production writes.
- Validate platform behavior in a licensed sandbox before treating any workflow as production-ready.
- Store future credentials in Streamlit secrets only when an approved integration requires them.
