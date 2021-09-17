FROM python:3.8-slim-buster

ENV TELEGRAM_BOT_TOKEN="#"
ENV URL_COUNT="#"
ENV URL_REPORTS="#"
ENV BASIC_LOGIN="#"
ENV BASIC_PASS="#"

WORKDIR /app
COPY . .

RUN pip install requests

ENTRYPOINT python transactions.py
