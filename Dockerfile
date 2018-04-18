FROM python:3.6

ADD . /python-server

WORKDIR /python-server

EXPOSE 8000

ENV MONGO_URL mongodb://grupo2:123@ds249269.mlab.com

ENV MONGO_PORT 49269/heroku_5d6zh6jz

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD gunicorn -w 4 app:app --log-file=-
