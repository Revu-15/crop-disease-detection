# Deployment Guide

Complete guide for deploying the Crop Disease Detection system to various platforms.

## 📋 Table of Contents

- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [Kubernetes](#kubernetes)
- [Cloud Platforms](#cloud-platforms)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring & Logging](#monitoring--logging)
- [Security](#security)

## 🏠 Local Deployment

### Development Server

```bash
# Backend
export FLASK_ENV=development
python backend/app.py

# Frontend (separate terminal)
cd frontend
npm start
```

### Production Server (Gunicorn)

```bash
# Install Gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn --workers 4 \
         --worker-class sync \
         --bind 0.0.0.0:5000 \
         --timeout 120 \
         backend:app

# Or with Gevent for async
gunicorn --workers 4 \
         --worker-class gevent \
         --worker-connections 1000 \
         --bind 0.0.0.0:5000 \
         backend:app
```

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/crop-disease

upstream flask_app {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    listen 80;
    server_name crop-disease.local;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name crop-disease.local;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/crop-disease.crt;
    ssl_certificate_key /etc/ssl/private/crop-disease.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # API Proxy
    location /api/ {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # File upload
        client_max_body_size 100M;
    }

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Static files cache
    location ~* \.(js|css|png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Systemd Service

```ini
# /etc/systemd/system/crop-disease-api.service

[Unit]
Description=Crop Disease Detection API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/crop-disease-detection
Environment="PATH=/var/www/crop-disease-detection/venv/bin"
ExecStart=/var/www/crop-disease-detection/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/crop-disease-api.sock \
    backend:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable crop-disease-api
sudo systemctl start crop-disease-api
sudo systemctl status crop-disease-api
```

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
# Multi-stage build
FROM python:3.9-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Set PATH
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "backend:app"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: crop_disease_detection
      POSTGRES_USER: crop_user
      POSTGRES_PASSWORD: crop_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U crop_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    environment:
      DATABASE_URL: postgresql://crop_user:crop_password@postgres/crop_disease_detection
      FLASK_ENV: production
      SECRET_KEY: your_secret_key
    ports:
      - "5000:5000"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./backend/models:/app/backend/models
      - ./uploads:/app/uploads
    restart: unless-stopped

  frontend:
    build: ./frontend
    environment:
      REACT_APP_API_URL: http://localhost:5000/api
    ports:
      - "3000:3000"
    depends_on:
      - api
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
```

### Deploy with Docker Compose

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## ☸️ Kubernetes

### Deployment YAML

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crop-disease-api
  labels:
    app: crop-disease-api

spec:
  replicas: 3
  selector:
    matchLabels:
      app: crop-disease-api
  
  template:
    metadata:
      labels:
        app: crop-disease-api
    spec:
      containers:
      - name: api
        image: crop-disease-api:latest
        ports:
        - containerPort: 5000
        
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: crop-disease-secrets
              key: database-url
        
        - name: FLASK_ENV
          value: "production"
        
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        
        livenessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        
        readinessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
        
        volumeMounts:
        - name: models
          mountPath: /app/backend/models
      
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: crop-disease-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: crop-disease-api-service

spec:
  selector:
    app: crop-disease-api
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace crop-disease

# Create secrets
kubectl create secret generic crop-disease-secrets \
  --from-literal=database-url=postgresql://... \
  -n crop-disease

# Create persistent volume
kubectl apply -f k8s/pvc.yaml -n crop-disease

# Deploy
kubectl apply -f k8s/deployment.yaml -n crop-disease

# Check status
kubectl get pods -n crop-disease
kubectl get svc -n crop-disease

# View logs
kubectl logs -n crop-disease deployment/crop-disease-api
```

## ☁️ Cloud Platforms

### AWS Deployment

#### Using Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 crop-disease-detection

# Create environment
eb create crop-disease-prod

# Deploy
eb deploy

# Monitor
eb open  # Open in browser
eb logs  # View logs
```

#### Using EC2

```bash
# Launch EC2 instance
aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name my-key

# SSH into instance
ssh -i my-key.pem ec2-user@instance-ip

# Install dependencies
sudo yum update -y
sudo yum install -y python3 python3-pip nginx

# Clone and deploy
git clone https://github.com/Revu-15/crop-disease-detection.git
cd crop-disease-detection
pip install -r requirements.txt
```

### Google Cloud Deployment

#### Using Cloud Run

```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT-ID/crop-disease-api

# Deploy
gcloud run deploy crop-disease-api \
  --image gcr.io/PROJECT-ID/crop-disease-api \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2 \
  --set-env-vars DATABASE_URL=postgresql://...
```

#### Using App Engine

```yaml
# app.yaml
runtime: python39

env: standard

env_variables:
  FLASK_ENV: production
  DATABASE_URL: postgresql://...

handlers:
- url: /.*
  script: auto
```

Deploy:
```bash
gcloud app deploy
```

### Azure Deployment

#### Using App Service

```bash
# Create resource group
az group create --name crop-disease-rg --location eastus

# Create App Service plan
az appservice plan create --name crop-disease-plan \
  --resource-group crop-disease-rg \
  --sku B2

# Create web app
az webapp create --resource-group crop-disease-rg \
  --plan crop-disease-plan \
  --name crop-disease-api

# Deploy
az webapp deployment source config-zip \
  --resource-group crop-disease-rg \
  --name crop-disease-api \
  --src deploy.zip
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main, production]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest tests/ --cov

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t crop-disease-api:latest .
      
      - name: Push to Docker Hub
        run: |
          docker login -u ${{ secrets.DOCKER_USER }} -p ${{ secrets.DOCKER_PASS }}
          docker push crop-disease-api:latest

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Your deployment commands
          echo "Deploying..."
```

## 📊 Monitoring & Logging

### Prometheus Monitoring

```python
# backend/metrics.py
from prometheus_client import Counter, Histogram

# Metrics
prediction_counter = Counter('predictions_total', 'Total predictions')
prediction_duration = Histogram('prediction_duration_seconds', 'Prediction duration')
error_counter = Counter('errors_total', 'Total errors')

@prediction_duration.time()
def make_prediction(image):
    # Prediction logic
    pass
```

### ELK Stack Logging

```yaml
# docker-compose.yml (additions)
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
  environment:
    discovery.type: single-node

kibana:
  image: docker.elastic.co/kibana/kibana:7.14.0
  ports:
    - "5601:5601"

logstash:
  image: docker.elastic.co/logstash/logstash:7.14.0
  volumes:
    - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
```

## 🔒 Security

### Environment Variables

```bash
# .env (production)
FLASK_ENV=production
SECRET_KEY=your_very_secure_key_here
DATABASE_URL=postgresql://secure_connection
DEBUG=false
ALLOWED_HOSTS=yourdomain.com
```

### SSL/TLS

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365
```

### Firewall Rules

```bash
# UFW (Ubuntu)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

**Last Updated**: 2026-05-30
