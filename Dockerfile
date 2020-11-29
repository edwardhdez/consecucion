FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /django-docker
WORKDIR /django-docker
ADD . /django-docker/
RUN pip install --upgrade pip && pip install -r requirements.txt