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
