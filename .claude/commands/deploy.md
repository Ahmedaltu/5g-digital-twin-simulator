Build and deploy the full stack using Docker Compose.

1. Verify Docker is available:
   ```
   docker --version && docker compose version
   ```
2. Check that `Dockerfile.backend`, `Dockerfile.frontend`, and `docker-compose.yml` exist and look correct.
3. Build and start all services:
   ```
   docker compose up --build -d
   ```
4. Confirm containers are running:
   ```
   docker compose ps
   ```
5. Tail logs for 10 seconds to confirm healthy startup:
   ```
   docker compose logs --tail=50
   ```
6. Report the URLs:
   - Backend: http://localhost:8000
   - Dashboard: http://localhost:8501
7. If any container fails to start, show its logs and diagnose the issue.
