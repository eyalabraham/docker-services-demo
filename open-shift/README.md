# Deployment with OpenShift

> Use the latest release or select the v1.2 or higher branch

Deploying with OpenShift is identical to deploying with Kubernetes, but requires a few small adjustments in order to enable the application.

First, apply the OpenShift route by using ```oc apply openshift-route.yaml``` with the YAML file contained in this directory.

Finally, the underlying services are containerized to run as root. This is not best practice, and OpenShift will not allow containers to run as root by default. Before deploying, create an OpenShift project and [modify its attributes as describe here](https://docs.openshift.com/container-platform/3.11/admin_guide/manage_scc.html). This will allow the services to run as-is.