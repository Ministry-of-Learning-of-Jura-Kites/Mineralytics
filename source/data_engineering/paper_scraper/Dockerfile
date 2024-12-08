FROM python:3.13

WORKDIR /app

ADD ./requirements.txt ./requirements.txt

ADD ./main.py ./main.py

RUN pip install -r /app/requirements.txt

ENTRYPOINT python -u /app/main.py