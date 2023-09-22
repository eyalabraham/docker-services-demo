# Deployment with OpenShift

> Use the latest release or select the v1.2 or higher branch

Deploying with OpenShift is identical to deploying with Kubernetes, but requires a few small adjustments in order to enable the application.

Clone the repository using ```git clone``` CLI to a working directory on your OpenShift cluster management node.

First, edit the persistent volume claim (PVC) YAML file ```docker-demo-pvc.yaml``` to name the appropriate storage class to use for the application database.

Next, create a new project with ```oc new-project <name>``` and make sure the selected current project is set to the one you created. Deploy the application into the project namespace using ```oc apply -f .```

Finally, create a route in OpenShift by going to ```Administrator > Networking > Routes``` and then Create Route under your project (name space) name. The route YAML in this directory is only a sample for reference, do not apply it in your project!

For an automated deployment, login to you cluster with ```oc login [...]``` and run the ```ocpdeploy.sh``` script from the ```..\K8s-deployment``` directory.