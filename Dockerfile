FROM python:3.9.13-slim

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt


RUN mkdir -p /src
COPY . /src/

WORKDIR /src
CMD uvicorn main:app --host 0.0.0.0
