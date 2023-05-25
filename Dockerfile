FROM python:3.10.11-alpine

WORKDIR /app

COPY . /app

RUN apk add --no-cache \
    libressl-dev \
    musl-dev \
    libffi-dev \
    gcc \
    g++ && \
    apk add -U tzdata && \
    cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    date

RUN pip install pip pipenv --upgrade && \ 
    PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

# RUN pip install pipenv --upgrade && \
#     pipenv install && \
#     pipenv sync --system

CMD ["pipenv","run", "python", "src/helm_iddle_cleaner.py"]