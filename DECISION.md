
### 5. DECISION.md
```markdown
# Architecture Decisions

## Nginx Configuration Strategy

### Upstream Design
- Used `backup` directive for Green service to ensure it only receives traffic when Blue fails
- Implemented aggressive timeouts (`proxy_connect_timeout: 2s`, `proxy_read_timeout: 5s`) for fast failure detection
- Configured `max_fails=2` and `fail_timeout=5s` to quickly mark unhealthy upstreams

### Failover Mechanism
- `proxy_next_upstream` handles retries to backup server within the same client request
- Combination of `error`, `timeout`, and `http_5xx` conditions for comprehensive failure detection
- 10-second total timeout ensures requests don't exceed the constraint

### Header Preservation
- Used `proxy_pass_header` to ensure application headers are forwarded unchanged
- No header manipulation to maintain app identity headers

## Health Checking Strategy
- Implemented Docker healthchecks for container orchestration awareness
- Used Nginx's built-in upstream health monitoring for request-level failover
- Separate health check endpoint for monitoring without affecting main traffic

## Performance Considerations
- `proxy_buffering off` to reduce latency and memory usage
- Conservative worker connections suitable for the scale
- Minimal logging on health endpoints to reduce I/O

## Trade-offs
- Aggressive timeouts may cause false positives in high-latency environments
- Simple backup strategy vs more complex weighted load balancing
- No session persistence required for this stateless application