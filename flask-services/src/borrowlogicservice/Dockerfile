#
# Docker file to build an image for the library borrowing-logic service.
#
FROM python:3.6-slim-stretch

LABEL maintainer="Eyal Abraham <eyal.abraham@gmail.com>"

RUN apt-get update -y               \
    && rm -rf /var/lib/apt/lists/*
    
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5004

ENTRYPOINT [ "python", "./borrowlogicservice.py" ]