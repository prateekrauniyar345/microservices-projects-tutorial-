Read memory [](file:///Users/prateekrauniyar/Library/Application%20Support/Code/User/workspaceStorage/652e64c41d4becdc6ecda7733b5cf317/GitHub.copilot-chat/memory-tool/memories/repo/independent-deployment-system.md)

# Independent Microservices Deployment System - (ON BRANCH individual-scaling)

## Overview
A Flask-based microservices architecture where each service runs independently with its own Docker container, versioning, and potential CI/CD pipeline integration.

## Architecture

### Services
1. **User Service** (Port 5001)
   - Authentication and user management
   - LOGIN: `POST /api/user/login`
   - REGISTER: `POST /api/user/create`
   - HEALTH: `GET /health`

2. **Product Service** (Port 5002)
   - Product catalog management
   - GET: `GET /api/products` (all products with inventory > 0)
   - GET: `GET /api/product/<code>` (single product)
   - CREATE: `POST /api/product/create` (new product)
   - HEALTH: `GET /health`

3. **Order Service** (Port 5003)
   - Shopping cart and order management
   - GET: `GET /api/order` (current order)
   - ADD: `POST /api/order/add-item` (add to cart)
   - UPDATE: `POST /api/order/update` (update order)
   - CHECKOUT: `POST /api/order/checkout` (complete order)
   - HEALTH: `GET /health`

4. **Frontend Service** (Port 8080)
   - Flask web UI
   - Routes: home, login, register, products, checkout, thank-you
   - Health: `GET /health`

## Deployment Structure

### Each Service Directory (`services/[service-name]/`)
```
services/
├── user/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── user_service.py
│   ├── requirements.txt
│   ├── VERSION
│   ├── deploy.sh (for future CI/CD)
│   └── data/ (SQLite database - Git ignored)
├── product/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── product_service.py
│   ├── requirements.txt
│   ├── VERSION
│   ├── deploy.sh
│   └── data/
├── order/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── order_service.py
│   ├── requirements.txt
│   ├── VERSION
│   ├── deploy.sh
│   └── data/
└── frontend/ → app/ directory
```

## Configuration

### Dockerfile Pattern (All Services)
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY [service]_service.py .
EXPOSE 5010
CMD ["flask", "--app", "[service]_service", "run", "--host=0.0.0.0", "--port=5010", "--reload"]
```

### docker-compose.yml Pattern (All Services)
```yaml
services:
  [service]-service:
    build: .
    container_name: [service]-service
    ports:
      - "[host_port]:5010"
    volumes:
      - [service]-data:/data  # Named volume for database persistence
    environment:
      PYTHONUNBUFFERED: 1
      FLASK_ENV: development
      SERVICE_NAME: [service]
      SERVICE_VERSION: 1.0.0
    networks:
      - microservices-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5010/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped
```

## Versioning Strategy

Each service has a `VERSION` file in its directory:
```
1.0.0
```

Format: `MAJOR.MINOR.PATCH` (Semantic Versioning)
- Exposed via `/health` endpoint response
- Used for tracking service versions in logs

## Database Persistence

### Named Volumes (Docker)
- `user-data:/data` → SQLite user.db
- `product-data:/data` → SQLite products.db
- `order-data:/data` → SQLite orders.db

**Advantage**: Persists data across container restarts without macOS bind mount issues

## Key Features Implemented

### ✅ Completed
1. Independent deployment - each service runs separately
2. Health checks - `/health` endpoint on all services
3. Database persistence - named volumes for each service
4. Docker containerization - Dockerfile + docker-compose per service
5. Print statements visible in real-time
6. Flask auto-reload (`--reload` flag) for development
7. Inter-service communication via `host.docker.internal:[port]`
8. API clients updated for independent service discovery

### 🚀 Ready for CI/CD
- Empty `deploy.sh` stub in each service directory
- VERSION file per service for version tracking
- Individual docker-compose files enable:
  - GitHub Actions workflows per service
  - Separate build/test/deploy pipelines
  - Version-based tagging

## Running Services

### Start Individual Service (Terminal per service)
```bash
cd services/user && docker compose up --build
cd services/product && docker compose up --build
cd services/order && docker compose up --build
cd app && docker compose up --build
```

### Cleanup
```bash
# Stop all services
docker compose down

# Remove volumes (WARNING: deletes databases)
docker volume rm user-data product-data order-data

# Recreate with clean data
docker compose up --build
```

## API Communication

### Frontend → Microservices
Frontend uses `host.docker.internal:[port]` because:
- Frontend runs in Docker container
- Other services run independently (not on same compose network)
- `host.docker.internal` resolves to host machine from inside container (macOS/Docker Desktop)

**API Client URLs:**
- User: `http://host.docker.internal:5001/api/user/...`
- Product: `http://host.docker.internal:5002/api/products`
- Order: `http://host.docker.internal:5003/api/order/...`

## Future CI/CD Integration

Each service's `deploy.sh` can be triggered by:
- GitHub Actions workflow on `services/[service]/` path changes
- Semantic versioning tags (v1.0.1, v2.0.0, etc.)
- Automatic Docker image building per service
- Registry push (Docker Hub, ECR, etc.)

Example structure ready:
```
.github/workflows/
├── user-service.yml
├── product-service.yml
├── order-service.yml
└── frontend.yml
```

## Important Notes

- **macOS bind mount issue**: Volumes paths cause Docker Desktop errors
  - Solution: Use named volumes for persistence
  - Alternative: Move project to home directory for full hot-reload

- **Port mappings**: Each service has unique host port
  - 5001 → User
  - 5002 → Product
  - 5003 → Order
  - 8080 → Frontend
  - Container port 5010 (except frontend 5000)

- **Health checks**: All containers must expose `/health` endpoint
  - Docker monitors health and marks as "healthy" after 3 consecutive passes
  - Used for readiness verification in orchestration

## Summary

This deployment system provides:
1. ✅ Independent scaling - restart single service without others
2. ✅ Isolated development - change one service without rebuilding all
3. ✅ Clear versioning - track service versions separately
4. ✅ Database isolation - each service owns its data
5. ✅ CI/CD ready - structure supports automated pipelines
6. ✅ Production-like - uses containers, health checks, volumes
7. ✅ Developer-friendly - auto-reload, visible logs, easy local testing