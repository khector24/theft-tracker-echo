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

## Continuous Delivery

This project uses continuous delivery:

- GitHub Actions runs tests on every push
- Render automatically deploys the `main` branch after CI passes
- No manual deployment steps are required
