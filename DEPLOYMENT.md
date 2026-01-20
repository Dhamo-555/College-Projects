# 🌐 Web Deployment Guide for Spider Tutor

This guide covers deploying Spider Tutor to various web platforms.

## Quick Start Options

### 1. 🚀 Gradio Cloud (Easiest)
Free, instant deployment with Gradio.

```bash
# Install gradio if not already installed
pip install gradio

# Push to Gradio Cloud
gradio deploy --repo "College-Projects/spider-tutor"
```

**Pros:** 
- No setup required
- Free hosting
- Auto-scaling
- Public URL instantly

**Cons:**
- Limited customization
- Gradio-only interface

---

### 2. 🐳 Docker + Heroku (Recommended)

#### Prerequisites
- Heroku account (free tier available)
- Docker installed
- Heroku CLI

#### Deployment Steps

```bash
# 1. Create Heroku app
heroku create spider-tutor

# 2. Set environment variables
heroku config:set OPENAI_API_KEY=your-key-here
heroku config:set LLM_PROVIDER=openai
heroku config:set MODEL_NAME=gpt-4o-mini

# 3. Build and push Docker image
heroku stack:set container
git push heroku main

# 4. View logs
heroku logs --tail
```

#### Add Procfile (if needed)
Create `Procfile` in root:
```
web: python app.py
```

---

### 3. ☁️ Railway.app (Simple)

1. Connect GitHub repository
2. Add environment variables in dashboard
3. Deploy with one click

**Environment Variables:**
```
OPENAI_API_KEY=your-key
LLM_PROVIDER=openai
MODEL_NAME=gpt-4o-mini
PORT=7860
```

---

### 4. ☁️ Replit (Free)

1. Import from GitHub
2. Set environment variables in Secrets
3. Click Run

---

### 5. ☁️ Google Cloud Run (Pay-as-you-go)

```bash
# Build image
docker build -t spider-tutor .

# Tag for Google Cloud Registry
docker tag spider-tutor gcr.io/PROJECT-ID/spider-tutor

# Push to registry
docker push gcr.io/PROJECT-ID/spider-tutor

# Deploy
gcloud run deploy spider-tutor \
  --image gcr.io/PROJECT-ID/spider-tutor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key,LLM_PROVIDER=openai
```

---

### 6. ☁️ AWS Lambda + API Gateway

Using AWS Serverless Application Model (SAM):

```bash
# Install AWS CLI and SAM
# Create serverless app structure
sam init

# Deploy
sam deploy --guided
```

---

### 7. 🖥️ Self-Hosted VPS (Full Control)

#### On Ubuntu/Debian Server

```bash
# 1. SSH into server
ssh user@your-server-ip

# 2. Clone repository
git clone https://github.com/yourusername/College-Projects.git
cd College-Projects/spider_tutor

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
nano .env  # Add your API keys

# 6. Run with gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:7860 app:demo

# 7. (Optional) Use systemd for auto-restart
sudo nano /etc/systemd/system/spider-tutor.service
```

#### Systemd Service File
```ini
[Unit]
Description=Spider Tutor Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/user/College-Projects/spider_tutor
ExecStart=/home/user/College-Projects/spider_tutor/venv/bin/gunicorn -w 4 -b 0.0.0.0:7860 app:demo
Restart=always

[Install]
WantedBy=multi-user.target
```

---

### 8. 🐳 Docker Hub + GitHub Actions (CI/CD)

#### GitHub Actions Workflow
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Docker Hub

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push to Docker Hub
        uses: docker/build-push-action@v2
        with:
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/spider-tutor:latest
```

---

## Environment Variables

Create `.env` file with:

```env
# LLM Provider (openai, anthropic, ollama)
LLM_PROVIDER=openai

# OpenAI
OPENAI_API_KEY=sk-your-api-key

# Anthropic (optional)
ANTHROPIC_API_KEY=sk-ant-your-key

# Voice Settings
VOICE_ENABLED=false  # Disable for web deployment
TTS_ENGINE=gtts

# Model Settings
MODEL_NAME=gpt-4o-mini
MAX_TOKENS=2000
TEMPERATURE=0.7

# Gradio Settings
GRADIO_SHARE=false
```

---

## Performance Tips

1. **Caching**: Add Redis for conversation history
2. **Load Balancing**: Use multiple instances behind load balancer
3. **Rate Limiting**: Implement API rate limits
4. **Monitoring**: Use Sentry for error tracking
5. **Logging**: Use structured logging with timestamps

---

## Cost Comparison

| Platform | Cost | Setup Time |
|----------|------|-----------|
| Gradio Cloud | Free | 1 min |
| Heroku | $7-50/month | 10 min |
| Railway | $5-100/month | 5 min |
| Google Cloud Run | Pay per request | 15 min |
| AWS Lambda | Pay per request | 30 min |
| VPS (DigitalOcean) | $5-20/month | 20 min |
| Replit | Free | 2 min |

---

## Security Checklist

- [ ] Never commit `.env` with real API keys
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Monitor API usage and billing
- [ ] Implement rate limiting
- [ ] Add CORS restrictions
- [ ] Use API key rotation

---

## Troubleshooting

### Port already in use
```bash
lsof -i :7860
kill -9 <PID>
```

### Docker build fails
```bash
docker build --no-cache -t spider-tutor .
```

### Memory issues
```bash
# Increase swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Recommended Stack

For production deployment:
- **Frontend**: Gradio (included)
- **Backend**: Python + FastAPI (optional upgrade)
- **Database**: PostgreSQL (optional)
- **Cache**: Redis (optional)
- **Monitoring**: Prometheus + Grafana
- **Deployment**: Docker + Kubernetes (for scale)
- **DNS**: Cloudflare

---

## Support
For deployment help, refer to individual platform docs or GitHub Issues.
