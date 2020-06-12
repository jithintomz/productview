# pull official base image
FROM python:3.6.0-alpine

RUN apk update && apk add libpq

RUN apk add --virtual .build-deps gcc python3-dev \
    musl-dev postgresql-dev \
    && apk add libffi-dev openssl-dev

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Remove build dependencies
RUN apk del .build-deps

# copy project
COPY . /usr/src/app/

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
