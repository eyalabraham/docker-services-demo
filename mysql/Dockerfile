#
# Docker file to build an image for the catalog database service.
#
FROM mysql:5.7

LABEL maintainer="Eyal Abraham <eyal.abraham@gmail.com>"

#RUN apt-get update -y
#RUN rm -rf /var/lib/apt/lists/*

COPY . /docker-entrypoint-initdb.d/

EXPOSE 3306

