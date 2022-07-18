FROM python:3.8-slim
MAINTAINER Roland Zitny
COPY requirements.txt /root
RUN pip install --upgrade pip && pip install -r /root/requirements.txt
COPY app /consumption-collector
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/python", "/app/main.py"]