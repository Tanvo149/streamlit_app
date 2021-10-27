import yfinance as yf
import pandas as pd
from datetime import date

from google.cloud import bigquery

from google.oauth2 import service_account

key_path = "secret/key.json"
project_id = 'tvv-airflow-tutorial-demo'
table_id ='tvv-airflow-tutorial-demo.Apple.history'
credentials = service_account.Credentials.from_service_account_file(key_path)
client = bigquery.Client(project='tvv-airflow-tutorial-demo', credentials=credentials)

        #query_job = client.query(self.sql)
        #results = query_job.result() 

#client = bigquery.Client()

#QUERY = (
#    'SELECT * FROM `tvv-airflow-tutorial-demo.ARK_ETF.history`'
#    'LIMIT 10'
#)
#query_job = client.query(QUERY) 
#rows = query_job.result()

#for row in rows:
#    print(row)

START = "2021-10-01"
TODAY = date.today().strftime("%Y-%m-%d")

data = yf.download('aapl', START, TODAY)
data.reset_index(inplace=True)
df = pd.DataFrame(data)
df_new =df[['Date','Open']]
print(df_new.head(5))

job_config = bigquery.LoadJobConfig(
    create_disposition='CREATE_IF_NEEDED',
    write_disposition='WRITE_APPEND'
)

job = client.load_table_from_dataframe(
    df_new, table_id, job_config=job_config
)
job.result() 



#df.to_csv('/Users/tanpersonal/Documents/streamlit/test.csv')
