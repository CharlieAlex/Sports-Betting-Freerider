import os
from google.cloud import bigquery
import schema

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/Users/alexlo/Desktop/Project/Sport_Lottery/big-query.json"
)

client = bigquery.Client()

# Create result table
table_id = "sport-lottery-database.playsports.result"
table = bigquery.Table(table_id, schema=schema.result_schema)
table.time_partitioning = schema.date_partitioning
table = client.create_table(table)
print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

# Create total table
table_id = "sport-lottery-database.playsports.total"
table = bigquery.Table(table_id, schema=schema.pred_schema)
table.time_partitioning = schema.date_partitioning
table = client.create_table(table)
print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

# Create mainpush table
table_id = "sport-lottery-database.playsports.mainpush"
table = bigquery.Table(table_id, schema=schema.pred_schema)
table.time_partitioning = schema.date_partitioning
table = client.create_table(table)
print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

# Create total_result table
table_id = "sport-lottery-database.playsports.total_result"
table = bigquery.Table(table_id, schema=schema.pred_result_schema)
table.time_partitioning = schema.date_partitioning
table = client.create_table(table)
print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

# Create mainpush_result table
table_id = "sport-lottery-database.playsports.mainpush_result"
table = bigquery.Table(table_id, schema=schema.pred_result_schema)
table.time_partitioning = schema.date_partitioning
table = client.create_table(table)
print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))
