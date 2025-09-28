from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from pyspark.sql import SparkSession
from helpers.strava_callable import main

with DAG(
    dag_id='strava_wrapped',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=["test"]
) as dag:

    run_my_script = PythonOperator(
        task_id='run_strava_wrapped',
        python_callable=main
    )