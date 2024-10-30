# Dockerfile

FROM python:3.10-slim

WORKDIR /app

COPY test_client.py /app/

RUN pip install aio-pika

CMD ["python", "test_client.py"]
