# Theft Tracker Echo

## Production Monitoring

This application exposes monitoring endpoints suitable for production environments:

- **GET /health**
  - Verifies database connectivity
  - Returns HTTP 200 if healthy

- **GET /metrics**
  - uptime_seconds
  - total_requests
  - requests_per_second
  - incidents_created

These endpoints support observability and production monitoring requirements.
