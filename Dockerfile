FROM python:3.8

COPY ./app ./app
WORKDIR ./app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "main:server", "-b 0.0.0.0:8050"]
