FROM python:3.8

COPY ./app ./app
COPY requirements.txt ./app
WORKDIR ./app
RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["python", "./main.py"]
