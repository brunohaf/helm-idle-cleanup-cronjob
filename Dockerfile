FROM python:3.10-alpine as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS py-temp

RUN apk add --no-cache \
    libressl-dev \
    musl-dev \
    libffi-dev \
    gcc && \
    apk add -U tzdata && \
    cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    date

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

COPY --from=py-temp /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app
COPY . /app

CMD ["python", "src/helm_idle_cleaner.py"]
