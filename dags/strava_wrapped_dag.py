from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from pyspark.sql import SparkSession
from helpers.strava_callable import initialize_responses
import os
import json

def fetch_strava_data(**kwargs):
    from airflow.models import Variable
    ti = kwargs['ti']  # This is the TaskInstance

    activities = initialize_responses()

    output_path = "/opt/airflow/data/strava_activities.json"
    print(f"Writing activities to {output_path}")
    print(f"Pushing to XCom with key=activities_path")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(activities, f)

    ti.xcom_push(key="activities_path", value=output_path)

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

    fetch_activities >> spark_task

