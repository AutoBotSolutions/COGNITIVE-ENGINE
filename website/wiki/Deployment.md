# Deployment Guide

This guide covers deploying the Cognitive Engine in various environments.

## Table of Contents

- [Deployment Overview](#deployment-overview)
- [System Requirements](#system-requirements)
- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Checklist](#production-checklist)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Scaling Strategies](#scaling-strategies)
- [Backup and Recovery](#backup-and-recovery)

---

## Deployment Overview

The Cognitive Engine can be deployed in various configurations:

- **Local/Development**: Single instance for development and testing
- **Docker**: Containerized deployment for consistency
- **Cloud**: Cloud-native deployment on AWS, GCP, or Azure
- **Distributed**: Multi-instance deployment for high availability

## System Requirements

### Minimum Requirements

- **CPU**: 2 cores
- **RAM**: 4 GB
- **Storage**: 10 GB
- **Python**: 3.9+
- **OS**: Linux, macOS, or Windows

### Recommended Requirements

- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Storage**: 20+ GB SSD
- **Python**: 3.10+
- **OS**: Linux (Ubuntu 20.04+ recommended)

### Network Requirements

- **Outbound**: HTTPS access to LLM APIs (OpenAI, Anthropic)
- **Inbound**: Port 8000 (if dashboard enabled)
- **Bandwidth**: 1+ Mbps for API calls

## Local Deployment

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd cognitive_engine

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run tests
python run.py test

# Start engine
python run.py
```

### Production-Ready Local Setup

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv sqlite3

# Create dedicated user
sudo useradd -r -s /bin/false cognitive_engine

# Set up directory structure
sudo mkdir -p /opt/cognitive_engine
sudo chown cognitive_engine:cognitive_engine /opt/cognitive_engine

# Install application
cd /opt/cognitive_engine
sudo -u cognitive_engine python3.10 -m venv venv
sudo -u cognitive_engine venv/bin/pip install -r requirements.txt

# Configure systemd service
sudo tee /etc/systemd/system/cognitive-engine.service > /dev/null <<EOF
[Unit]
Description=Cognitive Engine Service
After=network.target

[Service]
Type=simple
User=cognitive_engine
WorkingDirectory=/opt/cognitive_engine
Environment="PATH=/opt/cognitive_engine/venv/bin"
ExecStart=/opt/cognitive_engine/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable cognitive-engine
sudo systemctl start cognitive-engine
```

## Docker Deployment

### Dockerfile

Create a `Dockerfile` in the project root:

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 cognitive_engine && \
    chown -R cognitive_engine:cognitive_engine /app
USER cognitive_engine

# Expose dashboard port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run application
CMD ["python", "run.py"]
```

### docker-compose.yml

Create a `docker-compose.yml` for easy deployment:

```yaml
version: '3.8'

services:
  cognitive-engine:
    build: .
    container_name: cognitive-engine
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DEFAULT_LLM_PROVIDER=${DEFAULT_LLM_PROVIDER:-openai}
      - MIN_ITERATIONS=${MIN_ITERATIONS:-3}
      - MAX_ITERATIONS=${MAX_ITERATIONS:-50}
      - ENABLE_DASHBOARD=${ENABLE_DASHBOARD:-true}
      - DASHBOARD_PORT=${DASHBOARD_PORT:-8000}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    volumes:
      - ./data:/app/data
      - ./cognitive_engine.db:/app/cognitive_engine.db
      - ./cognitive_engine.log:/app/cognitive_engine.log
    networks:
      - cognitive-network
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  cognitive-network:
    driver: bridge
```

### Building and Running

```bash
# Build image
docker build -t cognitive-engine:latest .

# Run with docker-compose
docker-compose up -d

# Run standalone
docker run -d \
  --name cognitive-engine \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e ANTHROPIC_API_KEY=your_key \
  -v $(pwd)/data:/app/data \
  cognitive-engine:latest

# View logs
docker logs -f cognitive-engine

# Stop container
docker stop cognitive-engine
docker rm cognitive-engine
```

## Cloud Deployment

### AWS Deployment

#### Using EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 20.04 LTS
   - Instance Type: t3.medium (2 vCPU, 4 GB RAM)
   - Storage: 20 GB GP2

2. **Security Groups**
   - Inbound: SSH (22), HTTP (80), HTTPS (443), Custom (8000)
   - Outbound: All traffic

3. **Deploy Application**
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt-get update

# Install Docker
sudo apt-get install docker.io docker-compose

# Clone repository
git clone <repository-url>
cd cognitive_engine

# Configure environment
cp .env.example .env
nano .env  # Add your API keys

# Deploy
docker-compose up -d
```

#### Using ECS

1. **Create ECR Repository**
```bash
aws ecr create-repository --repository-name cognitive-engine
```

2. **Build and Push Image**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag
docker build -t cognitive-engine .
docker tag cognitive-engine:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/cognitive-engine:latest

# Push
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/cognitive-engine:latest
```

3. **Create Task Definition**
```json
{
  "family": "cognitive-engine",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "cognitive-engine",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/cognitive-engine:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "your-key"
        },
        {
          "name": "ANTHROPIC_API_KEY",
          "value": "your-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/cognitive-engine",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform Deployment

#### Using Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/cognitive-engine

# Deploy to Cloud Run
gcloud run deploy cognitive-engine \
  --image gcr.io/PROJECT_ID/cognitive-engine \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key,ANTHROPIC_API_KEY=your_key
```

#### Using GKE

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cognitive-engine
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cognitive-engine
  template:
    metadata:
      labels:
        app: cognitive-engine
    spec:
      containers:
      - name: cognitive-engine
        image: gcr.io/PROJECT_ID/cognitive-engine:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai-key
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: anthropic-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

```bash
# Apply deployment
kubectl apply -f k8s/deployment.yaml

# Create service
kubectl expose deployment cognitive-engine --type=LoadBalancer --port 8000
```

### Azure Deployment

#### Using Azure Container Instances

```bash
# Create resource group
az group create --name cognitive-engine-rg --location eastus

# Create container instance
az container create \
  --resource-group cognitive-engine-rg \
  --name cognitive-engine \
  --image cognitive-engine:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8000 \
  --environment-variables \
    OPENAI_API_KEY=your_key \
    ANTHROPIC_API_KEY=your_key
```

## Production Checklist

### Pre-Deployment

- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Security audit completed
- [ ] Performance benchmarks met
- [ ] Backup strategy in place
- [ ] Monitoring configured
- [ ] Alerting configured
- [ ] Rollback plan documented

### Configuration

- [ ] Environment variables set correctly
- [ ] API keys secured (use secrets manager)
- [ ] Log level set to INFO or WARNING
- [ ] Debug features disabled
- [ ] Dashboard disabled or secured
- [ ] Memory limits configured
- [ ] Iteration limits appropriate
- [ ] Database backup configured

### Security

- [ ] HTTPS enabled
- [ ] Firewall rules configured
- [ ] API keys not in code
- [ ] Secrets manager configured
- [ ] Access controls in place
- [ ] Authentication configured (if needed)
- [ ] Rate limiting configured
- [ ] Input validation enabled

### Performance

- [ ] Load testing completed
- [ ] Caching configured
- [ ] Database indexed
- [ ] Connection pooling configured
- [ ] CDN configured (if applicable)
- [ ] Autoscaling configured (if applicable)
- [ ] Monitoring dashboards set up
- [ ] Performance baselines established

### Reliability

- [ ] Health checks configured
- [ ] Auto-restart configured
- [ ] Load balancing configured
- [ ] High availability setup
- [ ] Disaster recovery plan
- [ ] Backup schedule configured
- [ ] Monitoring alerts configured
- [ ] On-call rotation established

## Monitoring and Maintenance

### Health Checks

```python
# Add to dashboard/server.py
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### Metrics to Monitor

- **System Metrics**
  - CPU usage
  - Memory usage
  - Disk usage
  - Network I/O

- **Application Metrics**
  - Request rate
  - Response time
  - Error rate
  - Active connections

- **Cognitive Metrics**
  - Average iterations per query
  - Average confidence scores
  - Memory growth rate
  - Learning effectiveness

### Logging

Configure centralized logging:

```python
# Use structured logging
import json
import logging

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.name,
            "line": record.lineno
        }
        if hasattr(record, 'extra'):
            log_obj.update(record.extra)
        return json.dumps(log_obj)
```

### Alerting

Set up alerts for:
- High error rate (> 5%)
- High response time (> 10s)
- High memory usage (> 80%)
- High CPU usage (> 90%)
- Disk space low (< 10%)
- API key quota exceeded
- Database connection failures

## Scaling Strategies

### Horizontal Scaling

Run multiple instances behind a load balancer:

```yaml
# docker-compose.yml for scaling
version: '3.8'

services:
  cognitive-engine:
    image: cognitive-engine:latest
    deploy:
      replicas: 3
    environment:
      - ENABLE_DASHBOARD=false  # Disable dashboard on workers
```

### Vertical Scaling

Increase resources for single instance:

```yaml
services:
  cognitive-engine:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
```

### Database Scaling

For high-volume deployments:

- Use PostgreSQL instead of SQLite
- Implement read replicas
- Use connection pooling
- Cache frequently accessed data

### Caching Strategy

Implement caching for:

- LLM API responses
- Thought graph queries
- Memory lookups
- Pattern extraction results

```python
# Example Redis caching
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cached_llm_call(prompt):
    cache_key = f"llm:{hash(prompt)}"
    cached = redis_client.get(cache_key)
    if cached:
        return cached.decode('utf-8')
    
    result = llm_client.generate(prompt)
    redis_client.setex(cache_key, 3600, result)
    return result
```

## Backup and Recovery

### Database Backup

```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups/cognitive-engine"
DATE=$(date +%Y%m%d_%H%M%S)
DB_PATH="/app/cognitive_engine.db"

mkdir -p $BACKUP_DIR

# Backup database
cp $DB_PATH $BACKUP_DIR/cognitive_engine_$DATE.db

# Compress
gzip $BACKUP_DIR/cognitive_engine_$DATE.db

# Keep last 7 days
find $BACKUP_DIR -name "*.db.gz" -mtime +7 -delete
```

### Configuration Backup

```bash
# Backup environment configuration
cp .env $BACKUP_DIR/.env_$DATE.backup
```

### Recovery Procedure

1. Stop the service
2. Restore database from backup
3. Restore configuration
4. Verify integrity
5. Start the service
6. Run health checks

### Disaster Recovery

- Store backups in multiple locations
- Test recovery procedures regularly
- Document recovery steps
- Maintain recovery time objectives (RTO)
- Maintain recovery point objectives (RPO)

## Security Considerations

### API Key Management

- Never commit API keys to version control
- Use environment variables or secrets manager
- Rotate keys regularly
- Monitor key usage
- Revoke compromised keys immediately

### Network Security

- Use HTTPS for all communications
- Implement rate limiting
- Use firewall rules
- Configure VPC/network segmentation
- Use private networks where possible

### Application Security

- Validate all inputs
- Sanitize outputs
- Implement authentication (if needed)
- Use parameterized queries
- Keep dependencies updated
- Run security scans

### Data Security

- Encrypt sensitive data at rest
- Encrypt data in transit
- Implement access controls
- Audit data access
- Comply with data regulations

## Troubleshooting Deployment Issues

### Container Won't Start

**Symptoms**: Container exits immediately or won't start

**Solutions**:
- Check logs: `docker logs <container-name>`
- Verify environment variables
- Check resource limits
- Verify API keys are valid
- Check network connectivity

### High Memory Usage

**Symptoms**: Memory usage grows continuously

**Solutions**:
- Check memory limits in configuration
- Implement memory cleanup
- Check for memory leaks
- Reduce MAX_MEMORY_SIZE
- Restart service periodically

### Slow Performance

**Symptoms**: Slow response times

**Solutions**:
- Check system resources
- Implement caching
- Optimize database queries
- Reduce iteration limits
- Use faster LLM provider

### API Rate Limits

**Symptoms**: API calls failing with rate limit errors

**Solutions**:
- Implement exponential backoff
- Cache responses
- Use multiple API keys
- Reduce request frequency
- Upgrade API plan

## Support

For deployment issues:
- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- Check logs: `cognitive_engine.log`
- Review this documentation
- Check GitHub issues
