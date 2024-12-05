import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import dag

def print_hello():
    print("Hello, Airflow!")

@dag(
    dag_id="hello_airflow_test_dag",
    start_date=datetime.datetime(2024, 12, 5),
    schedule_interval=None,
)
def simple_dag():
    hello_task = PythonOperator(
        task_id="hello_task",
        python_callable=print_hello,
    )

simple_dag()