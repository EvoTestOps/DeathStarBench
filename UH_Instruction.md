# Deploy a Kubernetes cluster on upcloud
## Example setting:
<img width="468" alt="image" src="https://github.com/user-attachments/assets/883b140d-57e7-42cf-b46a-aa22be1bd140" />
<img width="468" alt="image" src="https://github.com/user-attachments/assets/aaedced1-4b96-431a-9a1c-321006d4d990" />
<img width="468" alt="image" src="https://github.com/user-attachments/assets/4851ca81-0711-40e3-85f3-89b232fd1aad" />
<img width="468" alt="image" src="https://github.com/user-attachments/assets/6888cd27-bb9c-4b25-b097-4872be66c5ab" />
<img width="468" alt="image" src="https://github.com/user-attachments/assets/84fc3925-d548-48e5-be5e-157481bcf080" />
<img width="468" alt="image" src="https://github.com/user-attachments/assets/32fc80bf-611c-41a6-9738-22a293c1c995" />
<img width="468" alt="image" src="https://github.com/user-attachments/assets/8c176533-b392-4d40-a5c1-73396384a5b2" />

**Ps: kubectl needs to be installed in advance:** [Official address](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)


# Deploy hotelReservation microservice system on upcloud
Follow the [readme](https://github.com/EvoTestOps/DeathStarBench/tree/master/hotelReservation) instructions to install
## Pre-requirements:
- Docker
- Docker-compose
- luarocks (apt-get install luarocks)
- luasocket (luarocks install luasocket)
## Before you start
Ensure that the necessary local images have been made:
 bash
  <path-of-repo>/hotelReservation/kubernetes/scripts/build-docker-images.sh
## Deploy services

```
kubectl apply -Rf <path-of repo>/hotelReservation/kubernetes/
```
Wait until the deployment is complete to view the result
```
kubectl get pods
```

# Locust test
## Install locust
```
sudo apt-get update 
sudo apt install python3-pip
pip3 install locust
export PATH=$PATH:$HOME/.local/bin
```
## Executing the test:
Watch for the external-IP of frontend:
```
kubectl get svc frontend -w
```
Then
```
locust -f locust.py --host=http://<your-external-IP-of-frontend>:5000 --headless -u 10 -r 2 -t 10s
```
_parameter description:--host means the address of host; --headless means not start the graphical interface and output the result in terminal;- u means the number of concurrent users; - r means the number of new users per second; -t means the duration of the test_

# Monitoring
## Metric
Go to the corresponding directory
```
cd <path-of-repo>/hotelReservation/prometheus
```

Create a configmap
```
kubectl create configmap prometheus-config --from-file=prometheus.yml
```
Apply related resources
```
kubectl apply -f node-exporter-service.yaml
kubectl apply -f node-exporter.yaml
kubectl apply -f prometheus-config.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f prometheus-rbac.yaml
kubectl apply -f prometheus-service.yaml
```
Gets the external IP of the prometheus service
```
kubectl get svc | grep prometheus
```
To see prometheus's UI, visit your own prometheus url. It should be the following structure:
_http://your-external-IP-of-prometheus:9090_
<img width="1251" alt="image" src="https://github.com/user-attachments/assets/ed2bff69-625a-4313-a5fb-760d2ff67325" />
Some sample query metrics
- CPU utilization
```
rate(node_cpu_seconds_total{mode="system"}[1m])
```
- Memory usage
```
node_memory_MemTotal_bytes - node_memory_MemFree_bytes

```
- Disk usage
```
node_filesystem_size_bytes - node_filesystem_free_bytes
```
Enter the query and click the "Execute" button to view the time series chart in the Graph TAB or the specific values in the Table TAB.
<img width="1248" alt="image" src="https://github.com/user-attachments/assets/9e9a9365-6d29-44db-b2ae-d7a790fbf104" />
<img width="1249" alt="image" src="https://github.com/user-attachments/assets/efaed359-38eb-472b-9db2-920dcd44329e" />

## Logs
Get pods name
```
kubectl get pods
```
View the specific pod logs
```
kubectl logs <pod's name>
```




