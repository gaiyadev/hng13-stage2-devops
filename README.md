# Blue/Green Deployment with Nginx Auto-Failover

## Overview

This project implements a Blue/Green deployment strategy with automatic failover using Nginx as a reverse proxy. The setup ensures zero-downtime deployments and automatic traffic switching when failures occur.

## Quick Start

1. **Clone and setup**

   ```bash
   git clone <https://github.com/gaiyadev/hng13-stage2-devops.git>
   cd project
   cp .env.example .env

   ```

2. Configure environment
   Edit .env with your image references and release IDs.

3. Deploy

```bash
docker-compose up -d
```

4. Verify deployment

```bash
curl http://localhost:8080/version
```

## Testing Failover

1. Initial state (Blue active)

```bash
curl http://localhost:8080/version
# Response: X-App-Pool: blue
```

2. Verify automatic failover

```bash
curl http://localhost:8080/version
# Response: X-App-Pool: green (automatic switch)
```

4. Stop chaos

```bash
curl -X POST http://localhost:8081/chaos/stop
```

### Architecture

- Nginx: Reverse proxy with upstream failover configuration
- Blue Service: Primary application instance (port 8081)
- Green Service: Backup application instance (port 8082)
- Health Checks: Automatic failure detection
- Retry Logic: Seamless failover within same client request

## Key Features

* Automatic health-based failover
* Zero failed client requests during failover
* Header preservation (X-App-Pool, X-Release-Id)
* Configurable timeouts and retry policies
* Docker Compose orchestration
