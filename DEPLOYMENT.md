# AG2 Multi-Agent System - Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Cloud-Specific Deployment](#cloud-specific-deployment)
6. [CI/CD Pipeline Setup](#cicd-pipeline-setup)
7. [Monitoring & Logging](#monitoring--logging)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
```bash
- Python 3.9 or higher
- Docker 20.10+
- Docker Compose 2.0+
- kubectl 1.25+
- Git 2.30+
- Node.js 16+ (for frontend if extended)
```

### Cloud Provider Setup

#### AWS
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)

# Install eksctl for EKS
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
```

#### GCP
```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Install GKE auth plugin
gcloud components install gke-gcloud-auth-plugin
```

#### Azure
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Install AKS CLI
az aks install-cli
```

---

## Local Development Setup

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd ag2-multi-agent-system
```

### Step 2: Create Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
python -c "import autogen; print('AG2 installed successfully')"
```

### Step 4: Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or vim, code, etc.
```

**Required Environment Variables:**
```bash
# Minimum required configuration
OPENAI_API_KEY=sk-your-key-here
GITHUB_TOKEN=ghp_your-token-here
GITHUB_USERNAME=your-username
DOCKER_USERNAME=your-docker-username
DOCKER_PASSWORD=your-docker-password
CLOUD_PROVIDER=aws  # or gcp, azure
```

### Step 5: Run Application
```bash
# Start Streamlit UI
streamlit run ui/streamlit_app.py

# Access at: http://localhost:8501
```

### Step 6: Test the System
```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=. tests/

# Generate coverage report
pytest --cov=. --cov-report=html tests/
```

---

## Docker Deployment

### Build Docker Image
```bash
# Build image
docker build -t ag2-multi-agent:latest .

# Verify image
docker images | grep ag2-multi-agent
```

### Run with Docker
```bash
# Run container
docker run -d \
  --name ag2-system \
  -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/projects:/app/projects \
  -v $(pwd)/logs:/app/logs \
  ag2-multi-agent:latest

# Check logs
docker logs -f ag2-system

# Stop container
docker stop ag2-system

# Remove container
docker rm ag2-system
```

### Docker Compose Deployment
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Push to Docker Registry
```bash
# Login to Docker Hub
docker login

# Tag image
docker tag ag2-multi-agent:latest your-username/ag2-multi-agent:v1.0.0

# Push image
docker push your-username/ag2-multi-agent:v1.0.0

# For private registry
docker tag ag2-multi-agent:latest registry.example.com/ag2-multi-agent:v1.0.0
docker push registry.example.com/ag2-multi-agent:v1.0.0
```

---

## Kubernetes Deployment

### Step 1: Setup Kubernetes Cluster

#### Local (Minikube)
```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start --cpus=4 --memory=8192

# Enable ingress
minikube addons enable ingress
```

#### AWS EKS
```bash
# Create EKS cluster
eksctl create cluster \
  --name ag2-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 4 \
  --managed

# Update kubeconfig
aws eks update-kubeconfig --region us-east-1 --name ag2-cluster
```

#### GCP GKE
```bash
# Create GKE cluster
gcloud container clusters create ag2-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-2 \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 5

# Get credentials
gcloud container clusters get-credentials ag2-cluster --zone us-central1-a
```

#### Azure AKS
```bash
# Create resource group
az group create --name ag2-resources --location eastus

# Create AKS cluster
az aks create \
  --resource-group ag2-resources \
  --name ag2-cluster \
  --node-count 3 \
  --node-vm-size Standard_D2s_v3 \
  --enable-managed-identity

# Get credentials
az aks get-credentials --resource-group ag2-resources --name ag2-cluster
```

### Step 2: Create Kubernetes Manifests

```bash
# Create k8s directory structure
mkdir -p k8s/{base,overlays/{dev,staging,prod}}
```

**k8s/namespace.yaml:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ag2-system
```

**k8s/configmap.yaml:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ag2-config
  namespace: ag2-system
data:
  APP_ENV: "production"
  LOG_LEVEL: "INFO"
  CLOUD_PROVIDER: "aws"
```

**k8s/secret.yaml:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ag2-secrets
  namespace: ag2-system
type: Opaque
stringData:
  OPENAI_API_KEY: "your-key-here"
  GITHUB_TOKEN: "your-token-here"
  DOCKER_PASSWORD: "your-password-here"
```

**k8s/deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ag2-multi-agent
  namespace: ag2-system
  labels:
    app: ag2-multi-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ag2-multi-agent
  template:
    metadata:
      labels:
        app: ag2-multi-agent
    spec:
      containers:
      - name: ag2-app
        image: your-registry/ag2-multi-agent:latest
        ports:
        - containerPort: 8501
          name: http
        env:
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: ag2-config
              key: APP_ENV
        envFrom:
        - secretRef:
            name: ag2-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 5
          periodSeconds: 5
```

**k8s/service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ag2-service
  namespace: ag2-system
spec:
  type: LoadBalancer
  selector:
    app: ag2-multi-agent
  ports:
  - port: 80
    targetPort: 8501
    protocol: TCP
```

**k8s/ingress.yaml:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ag2-ingress
  namespace: ag2-system
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: ag2.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ag2-service
            port:
              number: 80
```

### Step 3: Deploy to Kubernetes
```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Apply configurations
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# Deploy application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n ag2-system
kubectl get services -n ag2-system
kubectl get ingress -n ag2-system

# Check logs
kubectl logs -f deployment/ag2-multi-agent -n ag2-system
```

### Step 4: Setup Horizontal Pod Autoscaler
```bash
# Create HPA
kubectl autoscale deployment ag2-multi-agent \
  --namespace ag2-system \
  --cpu-percent=70 \
  --min=2 \
  --max=10

# Verify HPA
kubectl get hpa -n ag2-system
```

---

## Cloud-Specific Deployment

### AWS-Specific Configuration

#### Setup ECR Repository
```bash
# Create ECR repository
aws ecr create-repository --repository-name ag2-multi-agent

# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag ag2-multi-agent:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/ag2-multi-agent:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ag2-multi-agent:latest
```

#### Setup Load Balancer
```bash
# Install AWS Load Balancer Controller
kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"

helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=ag2-cluster
```

### GCP-Specific Configuration

#### Setup GCR
```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Tag and push
docker tag ag2-multi-agent:latest gcr.io/<project-id>/ag2-multi-agent:latest
docker push gcr.io/<project-id>/ag2-multi-agent:latest
```

### Azure-Specific Configuration

#### Setup ACR
```bash
# Create ACR
az acr create --resource-group ag2-resources \
  --name ag2registry --sku Basic

# Login to ACR
az acr login --name ag2registry

# Tag and push
docker tag ag2-multi-agent:latest ag2registry.azurecr.io/ag2-multi-agent:latest
docker push ag2registry.azurecr.io/ag2-multi-agent:latest
```

---

## CI/CD Pipeline Setup

### GitHub Actions Workflow

**.github/workflows/deploy.yml:**
```yaml
name: Build and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: docker.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: pytest tests/ -v --cov=.

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    - name: Login to Registry
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBE_CONFIG }}
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/namespace.yaml
        kubectl apply -f k8s/configmap.yaml
        kubectl apply -f k8s/deployment.yaml
        kubectl apply -f k8s/service.yaml
        kubectl rollout status deployment/ag2-multi-agent -n ag2-system
```

### Setup GitHub Secrets
```bash
# Required secrets in GitHub repository settings:
DOCKER_USERNAME
DOCKER_PASSWORD
KUBE_CONFIG
OPENAI_API_KEY
GITHUB_TOKEN
AWS_ACCESS_KEY_ID (if using AWS)
AWS_SECRET_ACCESS_KEY (if using AWS)
```

---

## Monitoring & Logging

### Prometheus & Grafana Setup
```bash
# Add Prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace

# Port forward Grafana
kubectl port-forward -n monitoring \
  svc/prometheus-grafana 3000:80
```

### ELK Stack for Logging
```bash
# Install Elasticsearch
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch -n logging --create-namespace

# Install Kibana
helm install kibana elastic/kibana -n logging

# Install Filebeat
helm install filebeat elastic/filebeat -n logging
```

---

## Troubleshooting

### Common Issues

#### Pods Not Starting
```bash
# Check pod status
kubectl get pods -n ag2-system

# Describe pod
kubectl describe pod <pod-name> -n ag2-system

# Check logs
kubectl logs <pod-name> -n ag2-system

# Common fixes:
# 1. Check resource limits
# 2. Verify secrets/configmaps
# 3. Check image pull policy
```

#### Connection Issues
```bash
# Test service connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -- sh
# Inside pod:
wget -O- http://ag2-service.ag2-system.svc.cluster.local

# Check DNS
nslookup ag2-service.ag2-system.svc.cluster.local
```

#### Performance Issues
```bash
# Check resource usage
kubectl top pods -n ag2-system
kubectl top nodes

# Scale deployment
kubectl scale deployment ag2-multi-agent -n ag2-system --replicas=5
```

---

## Post-Deployment Verification

### Health Checks
```bash
# Check application health
curl http://<external-ip>/_stcore/health

# Test workflow execution
curl -X POST http://<external-ip>/api/workflow \
  -H "Content-Type: application/json" \
  -d '{"task": "test", "type": "text"}'
```

### Performance Testing
```bash
# Install k6
brew install k6  # Mac
# or
sudo apt-get install k6  # Linux

# Run load test
k6 run load-test.js
```

---

## Backup and Disaster Recovery

### Backup Strategies
```bash
# Backup Kubernetes resources
kubectl get all -n ag2-system -o yaml > backup.yaml

# Backup persistent volumes
velero backup create ag2-backup --include-namespaces ag2-system

# Schedule regular backups
velero schedule create ag2-daily --schedule="0 2 * * *" \
  --include-namespaces ag2-system
```

---

## Security Hardening

### Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ag2-network-policy
  namespace: ag2-system
spec:
  podSelector:
    matchLabels:
      app: ag2-multi-agent
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ag2-system
    ports:
    - protocol: TCP
      port: 8501
```

### Pod Security Policies
```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: ag2-psp
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
```

---

## Support and Documentation

For issues and questions:
- GitHub Issues: [Create Issue](https://github.com/your-repo/issues)
- Documentation: [Full Docs](https://your-docs-site.com)
- Email: support@example.com

---

**Deployment Guide Version 1.0.0**
**Last Updated: 2024**
