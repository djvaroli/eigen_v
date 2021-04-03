FROM python:3.8

COPY ./app ./app
WORKDIR ./app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "main:server", "-b 127.0.0.1:8050"]
