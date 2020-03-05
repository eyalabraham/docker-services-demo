# docker

Docker CLI [reference](https://docs.docker.com/engine/reference/commandline/docker/)

- ```docker image ls``` show all images
- ```docker build --rm --tag <name>:<tag> .``` build image from Dockerfile
- ```docker run --rm --volume <vol> --env <env> --name <name> -p <ext>:<int> --network <net> <image>:<tag> <command_line_args>``` run an image as a container
- ```docker network ls``` show networks
- ```docker <object> inspects <name>``` object is 'network' or 'image' etc.
- ```docker exec -it <name> [ bash | <shell cmd> ]``` execute a bash shell in a container in interactive tty, exit with Ctrl+p+q
- ```docker image ls eyalabraham/*:0.2 --format "{{.Repository}}:{{.Tag}}"``` list, filter and format image list

# docker-compose

- ```docker-compose up [ --build ]``` build and bring up
- ```docker-compose down``` bring down all resources
- ```docker-compose start``` start or,
- ```docker-compose stop``` stop without retaining last run temp image
- ```docker-compose logs [ --follow ]``` show container logs and optionally follow as they update

# [kubectl](https://kubernetes.io/docs/tutorials/)

- ```kubectl version``` show version of client and server
- ```kubectl cluster-info``` display cluster members

- ```kubectl get { nodes | pods | deployments | services }``` list participating objects (can use ```-l <selector>=<lable>``` with something such as app=MyApp)
- ```kubectl describe { nodes | pods | deployment | services }``` display human readable information
- ```kubectl logs <pod_name>``` retrieve STDOUT output for container in a pod, add ```--follow``` to stay attached
- ```Kubectl exec -ti <pod> [ bash | <shell cmd> ]``` similar to 'docker exec', but exit with 'exit'
- ```kubectl delete { nodes | pods | deployment | services }``` delete kubernetes objects
- ```kubectl create deployment NAME --image=image [--dry-run] [options]``` deploy a container image in a pod and run it (see 'docker ps')
- ```kubectl apply -f <dir>/``` start a deployment

- ```kubectl get pod -o=custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName --all-namespaces``` list pods' status and node allocation, the ```-l``` switch works here too.
- ```kubectl get pod -o wide``` similar to above

# K8s notes & practices

- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Apply 'names' and 'labels' to objects deployments so that field selectors can be used to filter with --field-selector](https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/), also [this](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/)
- [Persistent volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [ConfigMap for system setup parameters](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
- [Create network service between pods](https://kubernetes.io/docs/tasks/access-application-cluster/connecting-frontend-backend/)

# Lab deployment

1. Deploy app
   - Pod with sql_backend container will have a persistent volume resource for the database.
   - [Create a 'readiness probe' for a container?](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
     Alternative, [create an INIT container(s) in a pod](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
2. Is there a nice graphical UI to visualize the lab deployment?
3. How do we use cloud?
