# Docker Setup Guide

## What Was Fixed

1. **docker-compose.yml** - Now includes all services (frontend, user, product, order)
2. **Dockerfile** - Fixed the duplicate CMD lines
3. **Mock Services** - Created placeholder services so everything works without needing the actual microservices repos

## How to Run

### Step 1: Clean up any existing containers
```bash
cd /Volumes/ORICO/learnings/microservices/Hands-on-Microservices-with-Python
docker-compose down --volumes
```

### Step 2: Build and start all services
```bash
docker-compose up --build
```

You should see output from all 4 services starting.

### Step 3: Access the application
Open your browser and go to:
```
http://localhost:5000
```

## Test Credentials

The mock user service has a default user:
- **Username**: `john`
- **Password**: `password123`

## What Each Service Does

| Service | Port | Purpose |
|---------|------|---------|
| **frontend** | 5000 | Main web app (Flask) |
| **user** | 5001 | User authentication & registration |
| **product** | 5002 | Product catalog |
| **order** | 5003 | Shopping cart & checkout |

## How to Replace Mock Services with Real Ones

When you're ready to use the actual microservices from the separate repositories:

1. Clone the repositories into your workspace:
```bash
cd /Volumes/ORICO/learnings/microservices
git clone https://github.com/PacktPublishing/Hands-on-Microservices-with-Python-User-Service.git user_service
git clone https://github.com/PacktPublishing/Hands-on-Microservices-with-Python-Product-Service.git product_service
git clone https://github.com/PacktPublishing/Hands-on-Microservices-with-Python-Order-Service.git order_service
```

2. Update the `docker-compose.yml` to point to those repositories instead of the mock services

3. Update the build contexts in docker-compose.yml:
```yaml
user:
  build:
    context: ../user_service

product:
  build:
    context: ../product_service

order:
  build:
    context: ../order_service
```

## Troubleshooting

**Ports already in use?**
```bash
docker ps  # See what's running
docker kill <container_id>  # Kill any conflicting containers
```

**View logs for a specific service:**
```bash
docker-compose logs frontend  # or user, product, order
```

**Rebuild everything from scratch:**
```bash
docker-compose down --volumes
docker system prune
docker-compose up --build
```

## Docker Concepts Explained

- **Services**: Each service is like a mini-application running in its own container
- **Networks**: The `microservices-network` allows containers to talk to each other
- **Volumes**: `./app:/app` means changes to files on your computer are instantly seen in the container
- **Ports**: `5000:5010` means localhost:5000 → container:5010
- **depends_on**: Frontend waits for other services to start first
