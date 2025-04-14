FROM python:3.12-alpine

RUN mkdir -p /app/config

COPY source /app/source
COPY requirements.txt /app
COPY main.py /app
COPY template /app/template
COPY assets /app/assets

WORKDIR /app

RUN apk upgrade --no-cache

RUN apk add --no-cache --virtual build-deps  py3-pip build-base python3-dev libffi-dev openssl-dev gcc musl-dev
RUN pip install --no-cache --upgrade pip setuptools
RUN apk add --no-cache mariadb-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk del build-deps

USER 1001:1001
CMD ["python", "main.py"]