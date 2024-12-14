# from google.cloud import bigquery
# import os
#
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
#     "/Users/weichun.lo/Desktop/Project/Sports-Betting-Freerider/big-query.json"
# )
#
# client = bigquery.Client()
# table_id = "sport-lottery-database.playsports.mainpush"
# query = f"DELETE FROM `{table_id}` WHERE TRUE"
# query_job = client.query(query)
# query_job.result()
#
# print("所有行已删除")
