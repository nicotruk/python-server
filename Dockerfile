FROM python:3.6

ADD . /python-server

WORKDIR /python-server

RUN pip install --upgrade pip

RUN pip install -r requirements.txt