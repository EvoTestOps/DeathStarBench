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
Since Dashboard is a NodePort service, we can access it through the external IP of the node + the port number of the service. For example: [http://External_IP:Port](http://External_IP:Port)


Check the external IP(s) of nodes
```bash
kubectl get nodes -o wide
```
Check the port of chaos-daskport NodePort
```bash
kubectl get svc -n chaos-mesh
```
Your output will be something like this. In below the correct port number is 30820 
```bash
NAME                            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                                 AGE
chaos-daemon                    ClusterIP   None             <none>        31767/TCP,31766/TCP                     22m
chaos-dashboard                 NodePort    10.140.229.113   <none>        2333:30820/TCP,2334:32143/TCP           22m
chaos-mesh-controller-manager   ClusterIP   10.131.78.187    <none>        443/TCP,10081/TCP,10082/TCP,10080/TCP   22m
chaos-mesh-dns-server           ClusterIP   10.137.78.127    <none>        53/UDP,53/TCP,9153/TCP,9288/TCP         22m
```

<img width="600" alt="image" src="https://github.com/user-attachments/assets/19a487cd-9107-4af9-a855-bf1686525e63" />

 
Click  “Click here to generate” and follow its instruction, then you can get in the interface:
<img width="751" alt="Screenshot 2025-01-30 at 16 14 13" src="https://github.com/user-attachments/assets/eb377bac-e147-44de-b8d1-b8a652455270" />
<img width="752" alt="Screenshot 2025-01-30 at 16 14 34" src="https://github.com/user-attachments/assets/253dcb26-47c5-4921-886c-ff00eae18c52" />



> [!NOTE]
> Make sure get the correct account's token.
 
Then you can check corresponding experiment and related events.

<img width="1470" alt="image" src="https://github.com/user-attachments/assets/0724488a-083d-476a-a127-9fed93477578" />

## Create your own chaos experiment
It is recommended to configure the experiment by writing a YAML file. Please refer to the official documentation for the relevant [scope](https://chaos-mesh.org/docs/define-chaos-experiment-scope/) and [schedule rules](https://chaos-mesh.org/docs/define-scheduling-rules/).

If you want to rerun the experiment, use:
```bash
kubectl delete -f <corresponding_experiment.yaml>
```
Then, run the command again:
```bash
kubectl apply -f <corresponding_experiment.yaml>
```

