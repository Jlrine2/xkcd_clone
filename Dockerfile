FROM python:slim

WORKDIR /app

ADD app.py /app
ADD data.json /app
ADD scrape.py /app
COPY templates /app/templates
COPY static /app/static


ENV MAX_VAL=2237

COPY requirements.txt /app
RUN pip install -r requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0"]