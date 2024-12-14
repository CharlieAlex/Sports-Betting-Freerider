from google.cloud import bigquery
from google.cloud.bigquery.client import Client
import pandas as pd
import streamlit as st


@st.cache_resource(show_spinner=True)
def load_data(
    _client: Client,
    myquery: str,
) -> pd.DataFrame:
    query_job = _client.query(myquery)
    rows = query_job.result()
    df = rows.to_dataframe()
    df["date"] = pd.to_datetime(df["date"])
    print("load data")
    return df


if "__name__" == "__main__":
    bq_key = "/Users/weichun.lo/Desktop/Project/Sports-Betting-Freerider/big-query.json"

    client = bigquery.Client.from_service_account_json(json_credentials_path=bq_key)

    query_today_totalresult = """
        SELECT game, prediction, result
        FROM `sport-lottery-database.playsports.total_result`
        WHERE date = '2024-05-28'
    """

    load_data(client, query_today_totalresult)
