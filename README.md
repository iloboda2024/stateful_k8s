# Stateful Flask Application on Kubernetes

This application has been tested on a **DigitalOcean Kubernetes (DOKS)** cluster.

> **Note**
> The PostgreSQL deployment uses the default DigitalOcean StorageClass (`do-block-storage` or your configured `do` StorageClass).

---

## Prerequisites

Before deploying, ensure you have:

- Docker
- Kubernetes cluster
- `kubectl`
- Helm
- A container registry

---

# 1. Build and Push the Docker Image

Build the application image:

```bash
docker build -t stateful-flask:v0 -f task/Dockerfile .
```

Login to your container registry:

```bash
docker login
```

Tag the image:

```bash
docker tag stateful-flask:v0 <YOUR_REGISTRY>/stateful-flask:v0
```

Push the image:

```bash
docker push <YOUR_REGISTRY>/stateful-flask:v0
```

> Replace `<YOUR_REGISTRY>` with your Docker Hub username or container registry.

---

# 2. Deploy PostgreSQL

Deploy all Kubernetes resources:

```bash
kubectl apply -f kubernetes/*.yaml
```

---

# 3. Deploy the Flask Application

Create the namespace (if it doesn't already exist):

```bash
kubectl create namespace stateful-flask
```

Get the application pod:

```bash
pod=$(kubectl get pods \
    -n stateful-flask \
    -l app=stateful-flask \
    -o jsonpath='{.items[0].metadata.name}')
```

Initialize the database:

```bash
kubectl exec -it $pod -n stateful-flask -- flask db init
```

Generate the migration:

```bash
kubectl exec -it $pod -n stateful-flask -- flask db migrate
```

Apply the migration:

```bash
kubectl exec -it $pod -n stateful-flask -- flask db upgrade
```

---

# 4. Install NGINX Ingress Controller

Download Helm:

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4

chmod +x get_helm.sh

./get_helm.sh
```

Add the Ingress NGINX repository:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm repo update
```

Install the controller:

```bash
helm install nginx-ingress ingress-nginx/ingress-nginx \
    --namespace ingress-nginx \
    --create-namespace \
    --set controller.publishService.enabled=true
```

---

# 5. Test the API

Create a task:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "title":"Learn Flask",
        "description":"First task"
      }' \
  http://<LOAD_BALANCER_IP>/tasks
```

Replace `<LOAD_BALANCER_IP>` with the external IP or domain of your Ingress.

---

## Deployment Flow

```text
Build Docker Image
        │
        ▼
Push to Registry
        │
        ▼
Deploy PostgreSQL
        │
        ▼
Deploy Flask App
        │
        ▼
Run Database Migrations
        │
        ▼
Install NGINX Ingress
        │
        ▼
Access the API
```

---

## Notes

- Tested on **DigitalOcean Kubernetes (DOKS)**.
- PostgreSQL uses the DigitalOcean StorageClass.
- Update the image name in your Kubernetes manifests before deployment.
- Ensure your Ingress or LoadBalancer exposes the application before testing.
