# Phase 6: Optimization & Production Deployment (Week 6-7)

## Overview

**Status**: Ready to Start (After Phase 5 Complete)  
**Objective**: Deploy VitaCheck to production with containerization, orchestration, monitoring, and security hardening.

**Focus Areas**:
1. Docker containerization (frontend + backend + services)
2. Kubernetes orchestration (scaling, load balancing, health checks)
3. CI/CD pipeline (GitHub Actions, automated testing)
4. Production database (PostgreSQL migration from SQLite)
5. Monitoring & alerting (Prometheus, Grafana, ELK stack)
6. Security hardening (SSL/TLS, API authentication, secrets management)
7. Backup & disaster recovery

**Timeline**: Week 7-8 (10 working days)  
**Success Metrics**:
- ✅ 99.9% uptime SLA
- ✅ Auto-scaling (2-10 replicas)
- ✅ <500ms P95 latency at scale
- ✅ Fully automated deployment
- ✅ Production monitoring & alerting active

---

## Part 1: Docker Containerization

### 1.1 Backend Docker Image

Create `server/Dockerfile`:

```dockerfile
# Multi-stage build for optimization
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Build wheels
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install Python packages
RUN pip install --no-cache /wheels/*

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 vitacheck && chown -R vitacheck:vitacheck /app
USER vitacheck

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start application
CMD ["uvicorn", "streaming_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 1.2 Frontend Docker Image

Create `client/Dockerfile`:

```dockerfile
# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig*.json ./
COPY vite.config.ts ./
COPY index.html ./

# Install dependencies
RUN npm ci

# Copy source
COPY src ./src
COPY public ./public

# Build
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built app
COPY --from=builder /app/dist /usr/share/nginx/html

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:80/health || exit 1

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 1.3 Docker Compose (Development)

Create `docker-compose.yml`:

```yaml
version: '3.9'

services:
  # Backend API
  backend:
    build:
      context: ./server
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - OLLAMA_URL=http://ollama:11434
      - DATABASE_URL=postgresql://vitacheck:vitacheck@postgres:5432/vitacheck
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
      - ollama
    volumes:
      - ./server:/app  # Development only
      - ./server/chroma_db:/app/chroma_db
      - ./server/user_profiles:/app/user_profiles
    networks:
      - vitacheck-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend
  frontend:
    build:
      context: ./client
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - vitacheck-net
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=vitacheck
      - POSTGRES_PASSWORD=vitacheck_secure_password
      - POSTGRES_DB=vitacheck
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - vitacheck-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U vitacheck"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - vitacheck-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Ollama (LLM Server)
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    networks:
      - vitacheck-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
  redis_data:
  ollama_data:

networks:
  vitacheck-net:
    driver: bridge
```

---

## Part 2: Kubernetes Deployment

### 2.1 Kubernetes Manifests

Create `k8s/backend-deployment.yaml`, `k8s/frontend-deployment.yaml`, `k8s/postgres-statefulset.yaml`, `k8s/hpa.yaml`

(Full manifests provided in PHASE5_IMPLEMENTATION.md - copy those files)

---

## Part 3: CI/CD Pipeline

### 3.1 GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd server
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd server
          pytest tests/ -v --cov=. --cov-report=xml

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push backend
        uses: docker/build-push-action@v4
        with:
          context: ./server
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/backend:latest
```

---

## Phase 6 Checklist

### Week 7 (Days 1-5): Docker & Kubernetes

- [ ] Create backend Dockerfile with multi-stage builds
- [ ] Create frontend Dockerfile with Nginx
- [ ] Create docker-compose.yml for development
- [ ] Test Docker images locally
- [ ] Create Kubernetes manifests (deployment, service, config)
- [ ] Test K8s locally (minikube or kind)
- [ ] Create Horizontal Pod Autoscaler

### Week 8 (Days 1-5): CI/CD, Monitoring & Security

- [ ] Deploy Prometheus for metrics
- [ ] Deploy Grafana for dashboards
- [ ] Set up GitHub Actions workflows
- [ ] Configure automated testing (pytest)
- [ ] Implement secrets management
- [ ] Set up SSL/TLS certificates
- [ ] Configure network policies
- [ ] Implement API authentication (JWT tokens)
- [ ] Create PostgreSQL migration scripts
- [ ] Performance testing at scale
- [ ] Final production deployment

---

## Success Metrics - Phase 6

| Metric | Target | Status |
|--------|--------|--------|
| Container Images | 2 (backend, frontend) | Not Started |
| Kubernetes Replicas | 2-10 (autoscaling) | Not Started |
| Deployment Time | <5 minutes | Not Started |
| API Latency P95 | <500ms at scale | Not Started |
| Error Rate | <0.1% | Not Started |
| Uptime SLA | 99.9% | Not Started |
| Test Coverage | >80% | Not Started |
| Security Scan | Zero critical issues | Not Started |
| Backup Frequency | Daily | Not Started |
| Recovery Time (RTO) | <1 hour | Not Started |

---

**Phase 6 Status**: Ready to Start (After Phase 5)  
**Estimated Duration**: 10 working days  
**Target Completion**: End of Week 8

