from google.cloud import bigquery_datatransfer
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/Users/alexlo/Desktop/Project/Sport_Lottery/big-query.json"
)
transfer_client = bigquery_datatransfer.DataTransferServiceClient()

# The project where the query job runs is the same as the project
# containing the destination dataset.
project_id = "sport-lottery-database"
dataset_id = "playsports"
table_id = "total_result"

# This service account will be used to execute the scheduled queries. Omit
# this request parameter to run the query as the user with the credentials
# associated with this client.
# service_account_name = (
#     "sport-lottery-python@sport-lottery-database.iam.gserviceaccount.com"
# )
# 刪除這段才有辦法上傳


# Use standard SQL syntax for the query.
query_string = """
    SELECT
        total.game,
        total.prediction,
        total.count,
        total.rank,
        total.date,
        total.time,
        total.sport,
        total.during,
        result.result,
        result.outcome
    FROM
        `sport-lottery-database.playsports.total` total
    LEFT JOIN
        `sport-lottery-database.playsports.result` result
    ON
        total.game = result.game
        AND total.prediction = result.prediction
        AND total.date = result.date
    WHERE
        total.date = DATE_SUB(CURRENT_DATE('Asia/Taipei'), INTERVAL 1 DAY)
"""

parent = transfer_client.common_project_path(project_id)
first_run_time = datetime.datetime(2024, 5, 31, 17, 30, 0)
first_run_timestamp = Timestamp().FromDatetime(first_run_time)

transfer_config = bigquery_datatransfer.TransferConfig(
    destination_dataset_id=dataset_id,
    display_name="schedule_total_result",
    data_source_id="scheduled_query",
    params={
        "query": query_string,
        "destination_table_name_template": table_id,
        "write_disposition": "WRITE_APPEND",
        "partitioning_field": "date",
    },
    schedule="every 24 hours",
    schedule_options=bigquery_datatransfer.ScheduleOptions(
        start_time=first_run_timestamp
    ),
)

transfer_config = transfer_client.create_transfer_config(
    bigquery_datatransfer.CreateTransferConfigRequest(
        parent=parent,
        transfer_config=transfer_config,
    )
)

print("Created scheduled query '{}'".format(transfer_config.name))
