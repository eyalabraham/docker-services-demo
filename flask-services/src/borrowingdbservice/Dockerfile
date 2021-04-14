#
# Docker file to build an image for the borrowing database service.
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

# Add a new user with user id and change to non-root privilege
RUN useradd -u 8877 serenity
USER serenity

EXPOSE 5002

ENTRYPOINT [ "python", "./borrowingdbservice.py" ]