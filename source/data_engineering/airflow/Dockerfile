FROM apache/airflow:slim-2.10.3-python3.9

RUN pip install kafka-python

RUN airflow db init

CMD ["airflow","webserver"]