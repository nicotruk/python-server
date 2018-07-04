FROM python:3.6

ADD . /python-server

WORKDIR /python-server

EXPOSE 8000

ENV MONGO_URL mongodb://grupo2:123@ds249269.mlab.com

ENV MONGO_PORT 49269/heroku_5d6zh6jz

ENV APP_SERVER_NAME newModifiedName

ENV APP_SERVER_TOKEN eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoxLCJuYW1lIjoibmV3TW9kaWZpZWROYW1lIiwiaXNfYWRtaW4iOmZhbHNlfSwiaWF0IjoxNTMwMDc5NTkzfQ.wmvp-wtsP0_KGN7h2BNhF5eeE8qrSwAJZAqQX5AjW5Q

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD gunicorn -w 4 app:app --log-level=debug
