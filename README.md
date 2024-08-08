# MLops-Dummies

# Kubernetes Nginx StatefulSet Project

This repository contains a small Kubernetes project that demonstrates how to deploy a simple Nginx web application using a StatefulSet and expose it using a Service and optionally an Ingress. This project is ideal for learning and practicing Kubernetes concepts.

## Project Overview

- **StatefulSet**: Manages the deployment and scaling of a set of Pods, with unique, persistent identities and stable storage.
- **Service**: Exposes the Nginx application to the external world.
- **Ingress (Optional)**: Provides HTTP and HTTPS routing to services based on hostnames and paths.

## Prerequisites

1. **Minikube**: A tool to run Kubernetes locally.
2. **kubectl**: The Kubernetes command-line tool.
3. **Docker**: Required by Minikube to run Kubernetes containers.

## Setup

### 1. Start Minikube

First, make sure Minikube is installed and start your Minikube cluster:

```bash
minikube start
```

### 2. Configure `kubectl`

Ensure `kubectl` is configured to use the Minikube context:

```bash
kubectl config use-context minikube
```

## Deployment Steps

### 1. Create a StatefulSet

Create a file named `statefulset.yaml` with the following content:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nginx-statefulset
spec:
  serviceName: "nginx"
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          ports:
            - containerPort: 80
              name: web
          volumeMounts:
            - name: www
              mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
    - metadata:
        name: www
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi
```

Apply the StatefulSet configuration:

```bash
kubectl apply -f statefulset.yaml
```

### 2. Create a Service

Create a file named `service.yaml` with the following content:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

Apply the Service configuration:

```bash
kubectl apply -f service.yaml
```

### 3. (Optional) Create an Ingress

If you want to use Ingress, first enable the Ingress addon in Minikube:

```bash
minikube addons enable ingress
```

Create a file named `ingress.yaml` with the following content:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
spec:
  rules:
    - host: nginx.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx-service
                port:
                  number: 80
```

Apply the Ingress configuration:

```bash
kubectl apply -f ingress.yaml
```

### 4. Verify the Deployment

1. **Check Pods:**

   ```bash
   kubectl get pods
   ```

2. **Check Services:**

   ```bash
   kubectl get services
   ```

   If using a `LoadBalancer`, you can find the URL by running:

   ```bash
   minikube service nginx-service
   ```

3. **Check Ingress (Optional):**

   Modify your `/etc/hosts` file to point `nginx.local` to Minikube's IP:

   ```plaintext
   127.0.0.1 nginx.local
   ```

   Access the application at `http://nginx.local`.

## Git Repository

### 1. Initialize Git Repository

Initialize a new Git repository:

```bash
git init
```

### 2. Add Files to Repository

Add the configuration files to the repository:

```bash
git add statefulset.yaml service.yaml ingress.yaml
```

### 3. Commit Changes

Commit the changes:

```bash
git commit -m "Add Kubernetes configuration for Nginx StatefulSet and Service"
```

### 4. Push to Remote Repository

Create a new repository on GitHub or GitLab and push your code:

```bash
git remote add origin <URL-of-your-repository>
git push -u origin master
```

## Examples

### Scaling the Deployment

To scale the StatefulSet, use:

```bash
kubectl scale statefulset/nginx-statefulset --replicas=5
```
