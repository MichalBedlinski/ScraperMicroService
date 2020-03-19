FROM python:3.8-buster
LABEL maintainer="Michal Bedlinski"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update \
  && pip install -r requirements.txt \
  && apt-get clean

COPY . .

# Script for being sure mySQL server starts before we make migration
RUN git clone https://github.com/vishnubob/wait-for-it.git
