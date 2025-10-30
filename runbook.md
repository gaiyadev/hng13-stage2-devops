# Blue/Green Deployment Runbook

## Alerts and Operator Actions

### 1. Failover Detected Alert

**Message**: "Failover Detected - blue → green" (or vice versa)

**What it means**:

- The primary pool has failed health checks
- Nginx automatically switched traffic to the backup pool
- This is usually triggered by container crashes, high latency, or 5xx errors

**Operator Actions**:

1. Check primary pool health: `docker-compose ps app_blue` (or app_green)
2. Inspect logs: `docker-compose logs app_blue`
3. Check resource usage: `docker stats`
4. If issue is resolved, traffic will automatically return to primary after fail_timeout
5. For manual control, update ACTIVE_POOL in .env and restart

### 2. High Error Rate Alert

**Message**: "High Error Rate Alert - Current: X% | Threshold: Y%"

**What it means**:

- More than 2% of requests are returning 5xx errors in the last 200 requests
- This indicates potential application issues

**Operator Actions**:

1. Check application logs for both pools
2. Verify database/backend service connectivity
3. Check for recent deployments or configuration changes
4. Consider manual failover if errors persist
5. Monitor error patterns for root cause analysis

### 3. Alert Suppression

**Maintenance Mode**:
To suppress alerts during planned maintenance:

```bash
# Stop the watcher temporarily
docker-compose stop alert_watcher

# Perform maintenance
# Your maintenance commands here

# Restart watcher
docker-compose start alert_watcher
```
