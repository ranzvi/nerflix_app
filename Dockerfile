FROM python:3.8-slim

ARG GMAIL_ID=none
ARG GMAIL_PASSWORD=none
ARG EMAILS=none

ENV APP_HOME /netflix_app
ENV PIP_DEFAULT_TIMEOUT 100
ENV PYTHONPATH $PYTHONPATH:netflix_app


ENV GOOGLE_USER $GMAIL_ID
ENV GOOGLE_PASSWORD $GMAIL_PASSWORD
ENV EMAILS $EMAILS

WORKDIR $APP_HOME

COPY requirements.txt ./

RUN apt-get update
RUN apt-get -y install curl
RUN sh -c '/bin/echo -e "Y" | apt install build-essential'

RUN pip install -r ./requirements.txt

COPY netflix_app netflix_app/

CMD exec gunicorn --bind :${PORT-5000} --workers 1 --threads 8 netflix_app.run:app