import datetime
from airflow import DAG
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from utils import scrape_all
from airflow.models.param import Param

with DAG(
    dag_id="find_new_papers",
    start_date=datetime.datetime(2024, 12, 5),
    schedule="0 */5 * * *",
    catchup=False,
    render_template_as_native_obj=True,
) as dag:
    PythonOperator(
        task_id="find_new_papers",
        python_callable=scrape_all,
        op_args=[True],
        params={
            "stop_if_exists": Param(
                True,
                type="boolean",
            )
        },
    )
