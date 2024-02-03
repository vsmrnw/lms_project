FROM python:3.11.7-alpine
EXPOSE 8000
ARG ENV_FILE
WORKDIR /code

RUN apk update && apk add postgresql-dev python3-dev curl bash libpq-dev

ADD requirements.txt /code/requirements.txt

# copy wait-for-it script
COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /code
COPY .env /code/.env