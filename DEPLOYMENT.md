# Deployment Information

## Public URL
<<<<<<< HEAD
https://your-actual-agent-url.up.railway.app
=======
https://agent-day12-agent-deployment.up.railway.app
>>>>>>> ac1437c6f573d7055dae20928ce61429c63c1fb7

## Platform
Railway

## Test Commands

### 1. Health Check
```bash
curl https://your-actual-agent-url.up.railway.app/health
# Expected: {"status": "ok", "uptime": ..., "version": "1.0.0"}
```

### 2. Readiness Check
```bash
curl https://agent-lab12-nguyentiendung.up.railway.app/ready
# Expected: {"status": "ready"}
```

### 3. API Test (with authentication)
```bash
curl -X POST https://agent-lab12-nguyentiendung.up.railway.app/ask \
  -H "X-API-Key: dev-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{"question": "How to deploy an AI agent?"}'
```

## Environment Variables Set
- `PORT`: 8000
- `ENVIRONMENT`: production
- `AGENT_API_KEY`: dev-key-change-me (đã cấu hình trên Railway dashboard)
- `DAILY_BUDGET_USD`: 5.0
- `RATE_LIMIT_PER_MINUTE`: 20

## Screenshots
- Deployment dashboard
- Service logs
- Success test
