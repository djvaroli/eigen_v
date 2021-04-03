FROM python:3.8

COPY ./app ./app
WORKDIR ./app
RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["gunicorn", "main:server",  "-w", "2", "--threads", "2", "-b 0.0.0.0:8050"]
