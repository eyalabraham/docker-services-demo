# Kubernetes deployment
This directory includes YAML files needed for a kubernetes deployment. To deploy use ```kubectl apply -f .```. After deployment process completes wait for 20sec until the MySQL database initialized and then use your browser to view the projects at http://localhost:8000/
> If you are running the setup for the first time then images will be pulled from a public repository on [docker hub](https://hub.docker.com/u/eyalabraham).
> You must wait for all images to be pulled and for all pods to be in the ```Running``` state.
> You can check pod status by running ```kubectl get pods -l app=docker-demo```

## Deployments, Services and Pods topology
All deployments, services and pods are tagged with labels and you can filter them with the ```-l``` command line switch of ```kubectl```. Refer to the diagram below for details:
![k8s-deployment](../doc/image/k8s-deployment.png)