FROM apache/airflow:2.10.3

COPY ./requirements.txt /opt/airflow/requirements.txt

RUN pip install -r /opt/airflow/requirements.txt

ENTRYPOINT ["/bin/bash", "-c","airflow db init && airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin  && exec $0"]