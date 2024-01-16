FROM python:3.11-alpine3.19


COPY requirements.txt /requirements.txt
COPY mysite /
WORKDIR /mysite
EXPOSE 8000


RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /requirements.txt

RUN adduser --disabled-password admin-user

USER admin-user
