import datetime

from airflow import DAG
from airflow.decorators import dag
from airflow.operators.python import PythonOperator

from source.data_engineering.airflow.dags.utils import scrape_all


@dag(
    dag_id="test",
    start_date=datetime.datetime(2024, 12, 5),
    schedule=datetime.timedelta(seconds=30),
)
def generate_dag():
    # EmptyOperator(task_id="test")
    PythonOperator(
        task_id="test",
        provide_context=False,
        python_callable=scrape_all,
        op_args=[True],
    )


generate_dag()
