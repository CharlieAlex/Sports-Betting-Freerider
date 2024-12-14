from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/Users/weichun.lo/Desktop/Project/Sports-Betting-Freerider/big-query.json"
)

client = bigquery.Client()

# Create playsports dataset
dataset_id = "sport-lottery-database.playsports".format(client.project)
dataset = bigquery.Dataset(dataset_id)
dataset.location = "asia-southeast1"
dataset = client.create_dataset(dataset, timeout=30)
print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
