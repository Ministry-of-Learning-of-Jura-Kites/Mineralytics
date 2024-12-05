import datetime

from airflow import DAG
from airflow.decorators import dag
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty_operator import EmptyOperator

@dag(dag_id="test", start_date=datetime.datetime(2024, 12, 5), schedule=datetime.timedelta(seconds=30))
def generate_dag():
    EmptyOperator(task_id="test")
    # PythonOperator(dag=dag,
    #            task_id='test',
    #            provide_context=False,
    #            python_callable=my_python_function,
    #            op_args=['arguments_passed_to_callable'],
    #            op_kwargs={'keyword_argument':'which will be passed to function'})


generate_dag()
