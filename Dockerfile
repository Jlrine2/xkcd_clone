FROM python:3.8-slim

WORKDIR /app

ADD uwsgi.ini /app
ADD app.py /app
ADD data.json /app
ADD scrape.py /app
COPY templates /app/templates
COPY static /app/static


ENV MAX_VAL=0
RUN apt update -y && apt install -y gcc
COPY requirements.txt /app
RUN pip install -r requirements.txt

CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
