#
# Dockerfile for Django The Library demo project web fronend
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
# change owner on the app directory so that the local DB can be accessed
RUN useradd -u 8877 serenity
RUN chown -R serenity:serenity /usr/src/app
USER serenity

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver"]