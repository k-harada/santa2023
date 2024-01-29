from datetime import datetime, timezone
import os

import invoke
from google.cloud import bigquery


@invoke.task
def create_table(ctx, project: str = "kaggle-playground"):
    print("client")
    client = bigquery.Client(project=project)

    schema = [
        bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("seed", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("length", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("moves", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("job_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
    ]

    table = bigquery.Table(f"{project}.santa2023.cube", schema=schema)
    print("create...")
    table = client.create_table(table)
    print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))


@invoke.task
def solve(ctx, seed: int = 42):
    from rubik_large import large_cube

    job_id = os.environ.get("CLOUD_RUN_EXECUTION") or os.environ.get("CLOUD_ML_JOB_ID")

    id_list, moves_list = large_cube.solve(seed=seed)

    # Insert the results to BigQuery.
    rows_to_insert = [
        {
            "id": id_,
            "seed": seed,
            "length": len(moves.split(".")),
            "moves": moves,
            "timestamp": str(datetime.now(timezone.utc)),
            "job_id": job_id or "local",
        }
        for id_, moves in zip(id_list, moves_list)
    ]
    client = bigquery.Client()
    table_id = "kaggle-playground.santa2023.cube"
    errors = client.insert_rows_json(table_id, rows_to_insert)


@invoke.task
def solve_even(ctx, seed: int = 42):
    from rubik_large import large_cube_even

    job_id = os.environ.get("CLOUD_RUN_EXECUTION") or os.environ.get("CLOUD_ML_JOB_ID")

    id_list, moves_list = large_cube_even.solve(seed=seed)

    # Insert the results to BigQuery.
    rows_to_insert = [
        {
            "id": id_,
            "seed": seed,
            "length": len(moves.split(".")),
            "moves": moves,
            "timestamp": str(datetime.now(timezone.utc)),
            "job_id": job_id or "local",
        }
        for id_, moves in zip(id_list, moves_list)
    ]
    client = bigquery.Client()
    table_id = "kaggle-playground.santa2023.cube"
    errors = client.insert_rows_json(table_id, rows_to_insert)
