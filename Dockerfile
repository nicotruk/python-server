FROM python:2.7
ADD . /python-server
WORKDIR /python-server
RUN pip install -r requirements.txt