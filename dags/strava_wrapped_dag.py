from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from pyspark.sql import SparkSession
from helpers.strava_callable import initialize_responses
import os
import json
from langchain.llms import OpenAI
from airflow.models import Variable


def fetch_strava_data(**kwargs):
    ti = kwargs['ti']  # This is the TaskInstance

    activities = initialize_responses()

    output_path = "/opt/airflow/data/strava_activities.json"
    print(f"Writing activities to {output_path}")
    print(f"Pushing to XCom with key=activities_path")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(activities, f)

    ti.xcom_push(key="activities_path", value=output_path)



def push_stats_to_xcom(**kwargs):
    ti = kwargs['ti']

    with open("/opt/airflow/data/aggregated_activities.json") as f:
        stats = json.load(f)

    ti.xcom_push(key="runs", value=stats["runs"])
    ti.xcom_push(key="rides", value=stats["rides"])


with DAG(
    dag_id='strava_wrapped',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["test"]
) as dag:

    fetch_activities = PythonOperator(
        task_id='fetch_strava_activities',
        python_callable=fetch_strava_data
    )

    spark_task = BashOperator(
        task_id="run_spark_job",
        bash_command="""
        spark-submit /opt/airflow/dags/helpers/spark_summary.py "{{ task_instance.xcom_pull(task_ids='fetch_strava_activities', key='activities_path') }}"
        """
    )

    push_stats_task = PythonOperator(
        task_id="push_stats_xcom",
        python_callable=push_stats_to_xcom,
    )

    fetch_activities >> spark_task >> push_stats_task

