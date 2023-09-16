#FROM node:14-alpine AS client
#WORKDIR /app
#ADD frontend/package.json /app/package.json
#ADD frontend/package-lock.json /app/package-lock.json
#RUN npm ci --cache .npm --prefer-offline
#ADD frontend /app
#RUN npm run build

FROM python:3.11.4-alpine
EXPOSE 8000
ARG ENV_FILE
WORKDIR /code

RUN apk update && apk add mariadb-dev git gcc python3-dev musl-dev gettext curl jpeg-dev zlib-dev bash freetype-dev libjpeg-turbo-dev libpng-dev imagemagick imagemagick-dev libpq-dev

ADD requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD lms_project /code
# COPY /${ENV_FILE} /code/.env
COPY .env /code/.env
#COPY nginx.conf /etc/nginx/conf.d/nginx.conf
COPY entrypoint.sh /code/
RUN chmod +x /code/entrypoint.sh
CMD ["/code/entrypoint.sh"]