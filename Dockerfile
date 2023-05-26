FROM python:3.10.11-alpine

WORKDIR /app

COPY . /app

RUN apk --no-cache add \
    curl \
    openssl \
    bash \
    libressl-dev \
    musl-dev \
    libffi-dev \
    gcc \
    g++

RUN curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl \
    && curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 \
    && chmod +x get_helm.sh && ./get_helm.sh

RUN pip install pip pipenv --upgrade && \ 
    PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

CMD ["pipenv","run", "python", "src/helm_iddle_cleaner.py"]