import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import requests

#need update
# Create API client
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

st.sidebar.title("Options")

option = st.sidebar.selectbox("Which Dashboard?", ('wallstreetbets','chart','pattern','twitter','stockwits'))

if option == 'stockwits':
    symbol = st.sidebar.text_input("Symbol", max_chars=5)
    st.subheader('stockwits')

    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])

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

##for row in rows:
#st.write("check this data")
#    print(row)

#st.write(rows)