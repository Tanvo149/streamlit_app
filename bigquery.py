import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

#need update
# Create API client
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

option = st.selectbox("Which Dashboard?", ('wallstreetbets','chart','pattern'))

QUERY = (
    'SELECT * FROM `tvv-airflow-tutorial-demo.ARK_ETF.history`'
     'LIMIT 100'
)

@st.cache(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query(QUERY)

st.write("check this data")
for row in rows:
    print(row)

st.write(rows)