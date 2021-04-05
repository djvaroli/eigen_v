FROM python:3.8

COPY /app /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["bash", "./scripts/start.sh"]