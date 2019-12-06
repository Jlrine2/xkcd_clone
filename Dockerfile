FROM python:slim

ADD . /

ENV MAX_VAL=2237

RUN pip install -r requirements.txt

CMD ["python", "app.py"]