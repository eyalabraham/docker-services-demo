# Deployment with OpenShift

> Use the latest release or select the v1.2 or higher branch

Deploying with OpenShift is identical to deploying with Kubernetes, but requires a few small adjustments in order to enable the application.

First, create a route in OpenShift by going to ```Administrator > Networking > Routes``` and then Create Route under your project (name space) name. The route YAML in this directory is only a sample for reference, do not apply it in your project!

Finally, the underlying services might be containerized to run as root. This is not best practice, and OpenShift will not allow containers to run as root by default. Before deploying, create an OpenShift project and [modify its attributes as describe here](https://docs.openshift.com/container-platform/3.11/admin_guide/manage_scc.html). This will allow the services to run as-is.