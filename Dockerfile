FROM python:3.8

RUN apt-get update

RUN apt-get install cron -y

WORKDIR /app/

COPY ./requirements.txt /app/

RUN python3 -m pip install -r requirements.txt

COPY ./templates /app/templates
COPY ./main.py /app/
COPY ./functions.py /app/
COPY ./cron-job.txt /app/

RUN crontab /app/cron-job.txt

CMD ["cron", "-f"]