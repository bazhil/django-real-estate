FROM python:3.10.0-slim-buster

ENV = APP_HOME = /app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

LABEL maintainer='i-bazh@mail.ru'
LABEL description='Docker container for Real Estate Project, maded by tutorial: https://www.youtube.com/watch?v=9H9jr-sfHTo&t=7424s'

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y build_essential \
    && apt-get install -y gettext \
    && apt-get install -y netcat gcc postgresql \
    && apt-get purge --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* \

