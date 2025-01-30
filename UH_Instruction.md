# Deploy a Kubernetes cluster on upcloud
## Example setting:
<img width="468" alt="image" src="https://github.com/user-attachments/assets/883b140d-57e7-42cf-b46a-aa22be1bd140" />
<img width="468" alt="image" src="https://github.com/user-attachments/assets/aaedced1-4b96-431a-9a1c-321006d4d990" />
<img width="468" alt="image" src="https://github.com/user-attachments/assets/4851ca81-0711-40e3-85f3-89b232fd1aad" />
<img width="468" alt="image" src="https://github.com/user-attachments/assets/6888cd27-bb9c-4b25-b097-4872be66c5ab" />
<img width="468" alt="image" src="https://github.com/user-attachments/assets/84fc3925-d548-48e5-be5e-157481bcf080" />
<img width="468" alt="image" src="https://github.com/user-attachments/assets/32fc80bf-611c-41a6-9738-22a293c1c995" />

Install  kubectl: [https://kubernetes.io/docs/tasks/tools/install-kubectl-linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

Export KUBECONFIG that you downloaded above (use full path). 

Check that deploying kubernetes has worked. 

<img width="468" alt="image" src="https://github.com/user-attachments/assets/8c176533-b392-4d40-a5c1-73396384a5b2" />




# Deploy hotelReservation microservice system on upcloud

Clone the repo
```bash
git clone https://github.com/EvoTestOps/DeathStarBench.git
```

## Build docker images (Optional)
### Pre-requirements:
- Docker
- Docker-compose
- luarocks (apt-get install luarocks)
- luasocket (luarocks install luasocket)
### Before you start

Before deploying the services, you need to build the necessary Docker images:

1. Navigate to the scripts directory:
```bash
git clone https://github.com/EvoTestOps/DeathStarBench.git
cd DeathStarBench/hotelReservation/kubernetes/scripts
```
2. Build the Docker images using the provided script:
```bash
./build-docker-images.sh
```
> [!IMPORTANT]
> If you want to use your own Docker registry, you need to:
> - Open `build-docker-images.sh` and modify the `REGISTRY` variable to your Docker username
> - Update all deployment YAML files in the `kubernetes/` directory to use your modified image names
> - Example: Change `igorrudyk1/user-service:latest` to `your-username/user-service:latest`

## Deploy services

```bash
kubectl apply -Rf DeathStarBench/hotelReservation/kubernetes/
```
Wait until the deployment is complete to view the result
```bash
kubectl get pods
```

# Locust test
## Install locust
- Option.1: Using Conda
We strongly recommend using Conda virtual environment to avoid technical problems:
```bash
conda create --name hotel python=3.11
conda activate hotel
conda install -c conda-forge locust
```
- Option.2: Using pip
```bash
sudo apt-get update 
sudo apt install python3-pip
pip3 install locust
export PATH=$PATH:$HOME/.local/bin
```
## Executing the test:
Wait for the external-IP of frontend (might take up to 10 minutes):
```bash
kubectl get svc frontend -w
```
Then
```bash
locust -f uh_locust_tests/locust.py --host=http://<your-external-IP-of-frontend>:5000 --headless -u 10 -r 2 -t 10s
```
_parameter description:--host means the address of host; --headless means not start the graphical interface and output the result in terminal;- u means the number of concurrent users; - r means the number of new users per second; -t means the duration of the test_

# Monitoring
## Trace
Watch for the external-IP of jaeger:
```bash
kubectl get svc jaeger -w
```
To see Jaeger's UI, visit your own jaeger url. It should be the following structure:
_http://your-external-IP-of-jaeger:16686_

<img width="1246" alt="image" src="https://github.com/user-attachments/assets/7ff390aa-eb9f-488a-b6ce-8fe7e15db5b8" />
You can select different services from the service list to see the corresponding trace

## Metric
Go to the corresponding directory
```bash
cd <path-of-repo>/hotelReservation/UH_prometheus
```

Create a configmap
```bash
kubectl create configmap prometheus-config --from-file=prometheus.yml
```
Apply related resources
```bash
kubectl apply -f node-exporter-service.yaml
kubectl apply -f node-exporter.yaml
kubectl apply -f prometheus-config.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f prometheus-rbac.yaml
kubectl apply -f prometheus-service.yaml
```
Gets the external IP of the prometheus service
```bash
kubectl get svc | grep prometheus
```
To see prometheus's UI, visit your own prometheus url. It should be the following structure:
_http://your-external-IP-of-prometheus:9090_
<img width="1251" alt="image" src="https://github.com/user-attachments/assets/ed2bff69-625a-4313-a5fb-760d2ff67325" />
Some sample query metrics
- CPU utilization
```bash
rate(node_cpu_seconds_total{mode="system"}[1m])
```
- Memory usage
```bash
node_memory_MemTotal_bytes - node_memory_MemFree_bytes

```
- Disk usage
```bash
node_filesystem_size_bytes - node_filesystem_free_bytes
```
Enter the query and click the "Execute" button to view the time series chart in the Graph TAB or the specific values in the Table TAB.
<img width="1248" alt="image" src="https://github.com/user-attachments/assets/9e9a9365-6d29-44db-b2ae-d7a790fbf104" />
<img width="1249" alt="image" src="https://github.com/user-attachments/assets/efaed359-38eb-472b-9db2-920dcd44329e" />

## Logs
Get pods name
```bash
kubectl get pods
```
View the specific pod logs
```bash
kubectl logs <pod's name>
```

# Kubernetes Common Commands Sheet

## Pod Operations
```bash
# List all pods
kubectl get pods [-n namespace]

# Get pod details
kubectl describe pod <pod-name>

# Get pod logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>    # Follow log output

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/bash

# Delete pod
kubectl delete pod <pod-name>
```
## Service Operations
```
# List all services
kubectl get services
kubectl get svc    # Short form

# Get service details
kubectl describe service <service-name>

# Port forwarding
kubectl port-forward svc/<service-name> <local-port>:<service-port>
```
## Deployment Operations
```
# List deployments
kubectl get deployments

# Scale deployment
kubectl scale deployment <deployment-name> --replicas=<number>

# Rollout status
kubectl rollout status deployment/<deployment-name>

# Rollback deployment
kubectl rollout undo deployment/<deployment-name>
```
## Namespace Operations
```
# List namespaces
kubectl get namespaces
kubectl get ns    # Short form

# Create namespace
kubectl create namespace <namespace-name>

# Switch namespace
kubectl config set-context --current --namespace=<namespace-name>

# Delete namespace (and everything in it)
kubectl delete namespace <namespace-name>
```
> [!NOTE]
> Replace text in `<>` with your actual values.
> Add `-n <namespace>` to any command to specify a namespace.

