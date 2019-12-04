# Kubernetes deplyment
This directory includes YAML files needed for a kubernetes deployment. To deploy use ```kubectl apply -f .```. After deployment process completes wait for 20sec until the MySQL database initialized and then use your browser to view the projects at http://localhost:8000/

## Deplotment, Services and Pod topology
All deployments, services and pods are tagged with labes and you can filter them with kubectl ```-l``` command line switch. Refer to the diagram below for details:
![k8s-deployment](../doc/image/k8s-deployment.png)