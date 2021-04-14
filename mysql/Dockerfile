#
# Docker file to build an image for the catalog database service.
#
FROM mysql:5.7

LABEL maintainer="Eyal Abraham <eyal.abraham@gmail.com>"

RUN apt-get update -y               \
    && rm -rf /var/lib/apt/lists/*

COPY . /docker-entrypoint-initdb.d/

# Add a new user with user id and change to non-root privilege
RUN useradd -u 8877 serenity
USER serenity

EXPOSE 3306

