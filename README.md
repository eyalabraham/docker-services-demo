# Microservices, Containers, and Persistent Volume storage demo
This project contains a microservices architecture application. The application is a very (very) simple web-based book lending app for a fictitious library. The project is intended as a demonstration for a [Microservices architecture](https://microservices.io/) within a Containerized solution using [Docker Containers](https://www.docker.com/) and [Kubernetes](https://kubernetes.io/) orchestration.
The end goal is to deploy the demo with [persistent volumes](https://docs.docker.com/storage/) utilizing a [CSI driver](https://beta.docs.docker.com/ee/ucp/kubernetes/use-csi/), in order to demonstrate the ability to persist database data on an external block or file storage system.

> **Note:** this project was designed with extreme simplicity in mind, specifically to be used as a demo or a teaching/learning tool. Many liberties were taken with the architecture and the design in order to eliminate complexities such as security and scalability. This is not a secure, production quality, application but rather a learning or teaching tool for Microservices and Container technology; possibly also a reasonable starting point for a beginner or unexperienced programmer.

## Using the demo
The demo can be deployed on your laptop or on a Kubernetes cluster. For personal laptop use there are two modes to deploy the demo. The first using docker-compose and the second using Kubernetes available through a Docker Desktop setup. In order to deploy, first follow the two steps below, then follow the relevant section for the method you want to try.
1. Install Docker and Kubernetes desktop, for [Windows](https://www.docker.com/blog/docker-windows-desktop-now-kubernetes/) or [macOS](https://thenewstack.io/how-to-install-docker-desktop-with-kubernetes-on-macos/)
2. Select Branch tag v1.1
3. Pull the repository or [download and extract the v1.1 branch](https://github.com/eyalabraham/docker-services-demo/archive/v1.1.zip) zip file from GitHub into a new directory on your system.

### docker-compose deployment
1. Copy the ```sample.env``` file into a new file named ```.env```
```
cp sample.env .env
```
2. Optional, change the MySQL root password in the ```sample.env``` file.
3. Build the images and bring up the app services:
```
docker-compose up --detach --build 
```
4. Allow all services to start (check with ```docker ps``` under the STATUS table heading)
5. Point your web browser at: http://localhost:8000/ to access the library's web page.
6. Use the canned set of users in the ```mysql/patrons_demo.csv``` file to log into the library and borrow books
7. Display container logs during run time and watch activity when selecting web page links
```
docker-compose logs --follow
```
8. Shutdown and clean up
```
docker-compose down
```

### Kubernetes deployment
Use the latest release or select the v1.2 or higher branch, then follow [README.md](K8s-deployment/README.md) in the ```K8s-deployment``` directory.

### OpenShift deployment
Use the latest release or select the v1.2 or higher branch, then follow the Kubernetes deployment as well as review the notes in [README.md](open-shift/README.md) in the ```open-shift``` directory.

## Demoing and testing
A detailed demo script is available for you to use as a guide to familiarize with the application and basic underlying functions. [The demo script](doc/how-to-use-the-demo-app.md) includes a step by step description including screen shots.  
Wherever possible, internal ports where exposed to use as test points for the REST API endpoints. To test intermediate points within the application deploy the application with ```docker-compose``` and use the ```curl``` CLI command to "inject" REST requests directly into the running services. Suggested tests are listed in the TESTME.md files found in each of the services' directories. Refer to the [design.md](doc/design.md) files for RESTapi interface details. See the ```docker-compose.yml``` file for local port numbers under the ```ports:``` tag for each service.

## Services architecture

![Microservices architecture diagram](doc/image/architecture.png)

| Service              | Framework     | Description                                          |
|----------------------|---------------|------------------------------------------------------|
| Frontend             | Python/Django | Expose and HTTP server for accessing the application |
| Catalog database     | Python/Flask  | Back end book catalog database                       |
| Patrons database     | Python/Flask  | Back end patrons' registry database                  |
| Borrowing database   | Python/Flask  | Back end borrowing transaction database              |
| Borrowing service    | Python/Flask  | Library book borrowing logic                         |

## REST interface definitions and Microservices
See the [design.md](doc/design.md) file

## Dependencies
- Python3 (version 3.6.8)
- MySQL database server (version 5.7.27)
- Python dependencies in local ```requirements.txt``` files

## Resources
[Django web framework](https://www.djangoproject.com/), [Flask web framework](https://www.fullstackpython.com/flask.html)
[Python REST API CRUD Example using Flask and MySQL](https://www.roytuts.com/python-rest-api-crud-example-using-flask-and-mysql/), [MySQL Server on Ubuntu](https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu/), [Designing a RESTful API with Python and Flask](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask), [HTTP Status Codes](https://www.restapitutorial.com/httpstatuscodes.html)

