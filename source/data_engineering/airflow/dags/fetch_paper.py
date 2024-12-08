import datetime

from airflow import DAG
from airflow.decorators import dag
from airflow.operators.python import PythonOperator

from utils import scrape_all

with DAG(
    dag_id="find_new_papers",
    start_date=datetime.datetime(2024, 12, 5),
    schedule='*/30 * * * *',
    catchup=False,
) as dag:
    # EmptyOperator(task_id="test")
    PythonOperator(
        task_id="find_new_papers",
        python_callable=scrape_all,
        op_args=[True],
    ) 
