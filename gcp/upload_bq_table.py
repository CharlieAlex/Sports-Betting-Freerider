# Upload data from Gsheet to BigQuery
from google.cloud import bigquery
import schema
import polars as pl

gs_key = "/Users/alexlo/Desktop/Project/Sport_Lottery/big-query.json"


def upload_to_bigquery(client, df, table_id, table_schema):
    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=schema.set_job_config(table_schema),
    )
    job.result()
    print(f"Loaded {job.output_rows} rows to {table_id}.")


if __name__ == "__main__":
    table_id = "sport-lottery-database.playsports.result"
    client = bigquery.Client.from_service_account_json(json_credentials_path=gs_key)

    # upload result table
    df = (
        pl.read_csv("/Users/alexlo/Downloads/Sport Lottery Database result.csv")
        .filter(pl.col("game") != "NaN")
        .filter(~pl.all_horizontal(pl.all().is_null()))
        .to_pandas()
    )
    print(df.head())
    upload_to_bigquery(
        client,
        df,
        table_id="sport-lottery-database.playsports.result",
        table_schema=schema.result_schema,
    )

    # upload total table
    df = (
        pl.read_csv("/Users/alexlo/Downloads/Sport Lottery Database total.csv")[1:, :8]
        .select(pl.exclude(["t1", "t2", "t3", ""]))
        .filter(~pl.all_horizontal(pl.all().is_null()))
        .to_pandas()
    )
    print(df.head())
    upload_to_bigquery(
        client,
        df,
        table_id="sport-lottery-database.playsports.total",
        table_schema=schema.pred_schema,
    )

    # upload main push table
    df = (
        pl.read_csv("/Users/alexlo/Downloads/Sport Lottery Database main push.csv")[
            1:, :8
        ]
        .select(pl.exclude(["t1", "t2", "t3", ""]))
        .filter(~pl.all_horizontal(pl.all().is_null()))
        .to_pandas()
    )
    print(df.head())
    upload_to_bigquery(
        client,
        df,
        table_id="sport-lottery-database.playsports.mainpush",
        table_schema=schema.pred_schema,
    )

    # upload total_result table
    total = (
        pl.read_csv("/Users/alexlo/Downloads/Sport Lottery Database total.csv")[1:, :8]
        .select(pl.exclude(["t1", "t2", "t3", ""]))
        .filter(~pl.all_horizontal(pl.all().is_null()))
    )
    result = (
        pl.read_csv("/Users/alexlo/Downloads/Sport Lottery Database result.csv")
        .filter(pl.col("game") != "NaN")
        .filter(~pl.all_horizontal(pl.all().is_null()))
        .select(["date", "game", "prediction", "result", "outcome"])
    )
    df = total.join(result, on=["date", "game", "prediction"], how="inner").to_pandas()
    print(df.head())
    upload_to_bigquery(
        client,
        df,
        table_id="sport-lottery-database.playsports.total_result",
        table_schema=schema.pred_result_schema,
    )

    # upload mainpush_result table
    mainpush = (
        pl.read_csv("/Users/alexlo/Downloads/Sport Lottery Database main push.csv")[
            1:, :8
        ]
        .select(pl.exclude(["t1", "t2", "t3", ""]))
        .filter(~pl.all_horizontal(pl.all().is_null()))
    )
    result = (
        pl.read_csv("/Users/alexlo/Downloads/Sport Lottery Database result.csv")
        .filter(pl.col("game") != "NaN")
        .filter(~pl.all_horizontal(pl.all().is_null()))
        .select(["date", "game", "prediction", "result", "outcome"])
    )
    df = mainpush.join(
        result, on=["date", "game", "prediction"], how="inner"
    ).to_pandas()
    print(df.head())
    upload_to_bigquery(
        client,
        df,
        table_id="sport-lottery-database.playsports.mainpush_result",
        table_schema=schema.pred_result_schema,
    )
