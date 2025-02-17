FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y netcat

COPY shared-ledger-system/ .

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENV PYTHONPATH=/app

CMD ["/app/entrypoint.sh"]