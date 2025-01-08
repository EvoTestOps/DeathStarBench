# Install Chaos Mesh using Helm

## Install Helm
From Apt (Debian/Ubuntu)
```bash
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```
If you are using a different system or for a more detailed tutorial, check out this [link](https://helm.sh/docs/intro/install/)

To check whether Helm is installed or not, execute the following command:
```bash
helm version
```
## Install Chaos Mesh using Helm
Add the Chaos Mesh repository to the Helm repository:
```bash
helm repo add chaos-mesh https://charts.chaos-mesh.org
```
View the installable versions of Chaos Mesh
```bash
helm search repo chaos-mesh
```
Create the namespace to install Chaos Mesh
```bash
kubectl create ns chaos-mesh
```
Install Chaos Mesh 
```bash
helm install chaos-mesh chaos-mesh/chaos-mesh -n=chaos-mesh --set chaosDaemon.runtime=containerd --set chaosDaemon.socketPath=/run/containerd/containerd.sock --version 2.7.0
```
Verify the installation
```bash
kubectl get po -n chaos-mesh
```

# Run Chaos experiments

## Two one-time Chaos experiments
```bash
kubectl apply -f UH_network-delay.yaml
kubectl apply -f UH_pod-kill-exp.yaml
```

Please refer to the following [official website of chaos-mesh](https://chaos-mesh.org/docs/simulate-pod-chaos-on-kubernetes/) for more examples of experimental design
## Check results using Chaos Dashboard
Since Dashboard is a NodePort service, we can access it through the external IP of the node + the port number of the service. ***For example: http://\<External IP\>: 30951***

Check the external IP of nodes
```bash
kubectl get nodes -o wide
```

<img width="600" alt="image" src="https://github.com/user-attachments/assets/19a487cd-9107-4af9-a855-bf1686525e63" />

 
Click  “Click here to generate” and follow its instruction, then you can get in the interface:
<img width="600" alt="image" src="https://github.com/user-attachments/assets/13f51730-c164-4a6e-896f-d48168625666" />

 
You can check corresponding experiment and related events.



