FROM python:3.11-slim-bullseye

# LABELS
LABEL maintainer="Vitor Campos <vitorh45@gmail.com>"
LABEL application="agro"
LABEL repository="agro.git"

# Copy project main folder
COPY src/api api
COPY src/migrations migrations
COPY src/wsgi.py wsgi.py

COPY src/dependencies/requirements.txt requirements.txt

RUN apt-get update && apt-get install -qq -y libmariadb-dev libmariadb-dev-compat libpq-dev libssl-dev build-essential openssh-client libcurl4-openssl-dev
RUN pip install -r requirements.txt


RUN ls
COPY uwsgi.ini uwsgi.ini

## insert custom codes from application here

EXPOSE 5000
ENTRYPOINT ["uwsgi", "--ini", "./uwsgi.ini", "--enable-threads", "--single-interpreter", "--gevent", "100"]
