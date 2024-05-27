from google.cloud import bigquery

result_schema = [
    bigquery.SchemaField("game", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("prediction", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("result", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("outcome", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("date", "DATE", mode="NULLABLE"),
    bigquery.SchemaField("time", "TIME", mode="NULLABLE"),
    bigquery.SchemaField("sport", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("during", "STRING", mode="NULLABLE"),
]

pred_schema = [
    bigquery.SchemaField("game", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("prediction", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("count", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("rank", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("date", "DATE", mode="NULLABLE"),
    bigquery.SchemaField("time", "TIME", mode="NULLABLE"),
    bigquery.SchemaField("sport", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("during", "STRING", mode="NULLABLE"),
]


def set_job_config(schema: list):
    return bigquery.LoadJobConfig(
        schema=schema, autodetect=False, source_format=bigquery.SourceFormat.CSV
    )
