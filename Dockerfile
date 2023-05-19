FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install prometheus-api-client

CMD ["python", "helm_iddle_cleaner.py"]
