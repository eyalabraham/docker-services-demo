# Kubernetes cluster setup, the hard way

> These setup steps were compiled on December 2019. Be aware that code changes and later releases of any component may affect the procedure.
> The steps below were applied to three virtual machines installed with Red Hat Enterprise Linux Server release 7.7 (Maipo) running in a VMware ESX cluster. The virtual machines were configures as one Kubernetes master node and two worker nodes. The instructions should be applied to the master and worker nodes unless specified otherwise.

1. Check for unique MAC address and product UUD
```
ifconfig -a
sudo cat /sys/class/dmi/id/product_uuid
```
2. Name the host and the two nodes with appropriate host names
3. Create user name, enable it in the ```sudo``` group, and disable root
4. Update OS
```
yum -y update
```
5. Install dependencies
```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```
6. Add Docker repository
```
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```
7. Install Docker
```
sudo yum install docker
```
8. Start and then enable the Docker service
```
sudo systemctl start docker
sudo systemctl enable docker
```
9. Use an editor to create ```/etc/yum.repos.d/kubernetes.repo``` with the following content:
```
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg
       https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
```
10. Install kubelet, kubeadm, and kubectl
```
sudo yum install -y kubelet kubeadm kubectl
sudo systemctl enable kubelet
sudo systemctl start kubelet
```
11. Master node firewall settings. Note: port 6783 is required for Weave Net
```
sudo firewall-cmd --permanent --add-port=6443/tcp
sudo firewall-cmd --permanent --add-port=6783/tcp
sudo firewall-cmd --permanent --add-port=2379-2380/tcp
sudo firewall-cmd --permanent --add-port=10250/tcp
sudo firewall-cmd --permanent --add-port=10251/tcp
sudo firewall-cmd --permanent --add-port=10252/tcp
sudo firewall-cmd --permanent --add-port=10255/tcp
sudo firewall-cmd –-reload
```
12. Worker node firewall settings
```
sudo firewall-cmd --permanent --add-port=10251/tcp
sudo firewall-cmd --permanent --add-port=10255/tcp
sudo firewall-cmd --permanent --add-port=10250/tcp
sudo firewall-cmd --permanent --add-port=30000-32767/tcp
sudo firewall-cmd --permanent --add-port=6783/tcp
sudo firewall-cmd --reload
```
13. Update iptables, create ```/etc/sysctl.d/k8s.conf``` with:
```
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
```
14. Run ```sudo sysctl --system```
15. Disable SELinex
```
sudo setenforce 0
```
16. Edit file ```/etc/sysconfig/selinux``` and change line from ```SELINUX=permissive``` to ```disabled```
17. Disable swap
```
sudo sed -i '/swap/d' /etc/fstab
sudo swapoff -a
```
18. Initialize the master node
```
sudo kubeadm init
```
19. Note the discovery token from the command output (your token will be different)
```
Your Kubernetes control-plane has initialized successfully!

[...]

Join any number of worker nodes by running the following on each as root:

sudo kubeadm join 9.70.160.147:6443 --token hs41xr.tgon4xp0ddhr9xmf \
    --discovery-token-ca-cert-hash sha256:f3bae2fbdc9f5d67455239766d9716ff4ab38c42f31899fa1813316ef6a74efe 
```
20. Run the following steps as a regular user on the Master node
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
```
21. Setup Weave Net pod network; on the Master node run:
```
export kubever=$(kubectl version | base64 | tr -d '\n')
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$kubever"
```
22. Run ```sudo /usr/local/bin/weave status connections``` on all nodes and make sure that all network node connections are in the **established** state. If they are in a **failed** state double check your fire wall settings to make sure port 6783/tcp is open on all nodes.
23. Run ```kubectl get nodes``` on the Master node until you see k8s-master is in **Ready** state
24. Add nodes to the setup
  - By running the ```kubeadm join``` command on a node using the output from the ```kubeadm init```.
  - The ```join``` should be run with ```sudo``` on each __Worker node__ you wish to add to the cluster.
  - Run ```kubectl get nodes``` on the Master node to check that the worker nodes join and are ready. The ready state takes a while.
  - Worker nodes need to be prepared with steps #1 through #17 (except for step #11)
  - If adding nodes much later in the process the token might need to be regenerated. Use  ```kubeadm token create``` to generate a new tokem and and new SHA256 key with:
  ```
  openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
  ```
   - The join command format is ```kubectl join <master_node>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<key>```
