FROM python:2.7-stretch

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8080
