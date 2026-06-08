# Deployment Guide - OnePiece API with Mindfighter

## 🚀 Quick Deployment

### Local Development
```bash
# 1. Clone & setup
git clone <repo>
cd oNEPIECE

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run development server
uvicorn main:app --reload

# 5. Access
# Dashboard: http://localhost:8000/
# API Docs: http://localhost:8000/docs
```

---

## 🐳 Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build & Run
```bash
# Build image
docker build -t onepiece-api:latest .

# Run container
docker run -p 8000:8000 onepiece-api:latest
```

### Docker Compose
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=info
    volumes:
      - ./logs:/app/logs
```

---

## ☁️ Cloud Deployment

### Heroku
```bash
# 1. Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 2. Deploy
heroku create onepice-api
heroku config:set PYTHONUNBUFFERED=1
git push heroku main
```

### AWS Lambda
```bash
# Use serverless framework
serverless deploy --function api
```

### Google Cloud Run
```bash
# Deploy
gcloud run deploy onepiece-api \
  --source . \
  --platform managed \
  --region us-central1
```

---

## 📊 Production Configuration

### Multi-Worker Setup
```bash
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker
```

### Gunicorn + Uvicorn
```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

## 🔒 Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set up rate limiting
- [ ] Configure CORS properly
- [ ] Add authentication if needed
- [ ] Enable logging and monitoring
- [ ] Use reverse proxy (Nginx/Apache)
- [ ] Regular security updates
- [ ] Backup database regularly

---

## 📈 Monitoring & Logging

### Logging Setup
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Health Checks
```bash
# Monitor API health
watch -n 10 'curl http://localhost:8000/health'
```

---

## 📦 Environment Variables

Create `.env` file:
```
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=your-secret-key
LOG_LEVEL=info
CORS_ORIGINS=https://example.com
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest
      - name: Deploy
        run: |
          docker build -t api .
          # Push to registry and deploy
```

---

**Ready for production deployment! 🚀**
