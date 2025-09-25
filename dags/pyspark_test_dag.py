from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from pyspark.sql import SparkSession

def run_spark_job():
    spark = SparkSession.builder \
        .appName("AirflowPySpark") \
        .master("local[*]") \
        .getOrCreate()

    data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
    df = spark.createDataFrame(data, ["name", "age"])
    df.show()
    spark.stop()

default_args = {
    'start_date': datetime(2023, 1, 1),
    'catchup': False,
}

dag = DAG('pyspark_test_dag', default_args=default_args, schedule_interval=None)

run_spark = PythonOperator(
    task_id='run_spark_job',
    python_callable=run_spark_job,
    dag=dag,
)
