# Security Guide

This guide covers security considerations and best practices for deploying and using the Cognitive Engine.

## Table of Contents

- [Security Overview](#security-overview)
- [API Key Management](#api-key-management)
- [Data Security](#data-security)
- [Network Security](#network-security)
- [Application Security](#application-security)
- [Agent Security](#agent-security)
- [Memory Security](#memory-security)
- [Deployment Security](#deployment-security)
- [Compliance](#compliance)
- [Security Auditing](#security-auditing)

---

## Security Overview

The Cognitive Engine processes potentially sensitive information and interacts with external APIs. Security is critical for:

- Protecting API keys and credentials
- Securing user data and queries
- Preventing unauthorized access
- Ensuring safe agent behavior
- Maintaining data privacy
- Complying with regulations

### Security Principles

1. **Least Privilege**: Components have only necessary access
2. **Defense in Depth**: Multiple layers of security
3. **Secure by Default**: Safe configurations out of the box
4. **Transparency**: Security practices are documented
5. **Continuous Improvement**: Regular security updates

---

## API Key Management

### Storing API Keys

**Never commit API keys to version control**

❌ **Wrong**:
```bash
# .env file committed to git
OPENAI_API_KEY=sk-actual-key-here
```

✅ **Correct**:
```bash
# .env.example with placeholders
OPENAI_API_KEY=your_openai_api_key_here

# .env file in .gitignore
OPENAI_API_KEY=sk-actual-key-here
```

### Using Environment Variables

```bash
# Set environment variables
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"

# Or use .env file
echo "OPENAI_API_KEY=your-key" > .env
```

### Using Secrets Managers

For production deployments, use a secrets manager:

#### AWS Secrets Manager

```python
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

api_key = get_secret('cognitive-engine/openai-api-key')
```

#### HashiCorp Vault

```python
import hvac

client = hvac.Client(url='https://vault.example.com')
client.auth.approle.login(role_id='your-role', secret_id='your-secret')
api_key = client.read('secret/cognitive-engine/openai')['data']['value']
```

#### Environment Variable Injection

```yaml
# Kubernetes Secret
apiVersion: v1
kind: Secret
metadata:
  name: api-keys
type: Opaque
stringData:
  openai-key: your-key
  anthropic-key: your-key
```

### Key Rotation

Regularly rotate API keys:

1. Generate new API key from provider
2. Update application configuration
3. Test with new key
4. Revoke old key
5. Monitor for issues

```bash
# Rotation script
#!/bin/bash
# Generate new key (manual step from provider)
NEW_KEY="new-key-here"

# Update configuration
sed -i "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$NEW_KEY/" .env

# Restart application
systemctl restart cognitive-engine

# Test
python run.py test

# If successful, revoke old key (manual step from provider)
```

### Key Scoping

Use scoped keys when possible:

```python
# OpenAI allows scoped keys
# Create key with specific permissions only
# - Read-only access
# - Specific models only
# - Rate limits
```

---

## Data Security

### Data at Rest

Encrypt sensitive data stored on disk:

```python
from cryptography.fernet import Fernet
import os

class SecureStorage:
    def __init__(self, key=None):
        if key is None:
            key = os.environ.get('ENCRYPTION_KEY')
            if not key:
                key = Fernet.generate_key()
        self.cipher = Fernet(key)
    
    def encrypt(self, data):
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data).decode()

# Use for sensitive memory entries
storage = SecureStorage()
encrypted = storage.encrypt("sensitive data")
```

### Database Encryption

For SQLite, use SQLCipher or encrypt the entire file:

```bash
# Encrypt database file
openssl enc -aes-256-cbc -salt -in cognitive_engine.db -out cognitive_engine.db.enc

# Decrypt when needed
openssl enc -aes-256-cbc -d -in cognitive_engine.db.enc -out cognitive_engine.db
```

For production, use PostgreSQL with transparent data encryption (TDE).

### Data in Transit

Always use HTTPS/TLS:

```python
# Force HTTPS in web applications
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, force_https=True)
```

### Input Validation

Validate all user inputs:

```python
from pydantic import BaseModel, validator
import re

class QueryInput(BaseModel):
    query: str
    
    @validator('query')
    def validate_query(cls, v):
        # Length check
        if len(v) > 10000:
            raise ValueError("Query too long")
        
        # Content check
        if not re.match(r'^[\w\s\.,!?;:()-]+$', v):
            raise ValueError("Invalid characters")
        
        # SQL injection prevention
        dangerous = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER']
        if any(word in v.upper() for word in dangerous):
            raise ValueError("Potentially dangerous query")
        
        return v
```

### Output Sanitization

Sanitize outputs from LLMs:

```python
import html

def sanitize_output(text):
    """Sanitize LLM output to prevent XSS."""
    return html.escape(text)

# Or use a library
from bleach import clean

sanitized = clean(text, tags=[], attributes={})
```

### Data Retention

Implement data retention policies:

```bash
# Automatic cleanup script
#!/bin/bash
# Delete data older than 90 days
find /path/to/memory -name "*.db" -mtime +90 -delete
find /path/to/logs -name "*.log" -mtime +30 -delete
```

```python
# In application
from datetime import datetime, timedelta

def cleanup_old_memory():
    cutoff = datetime.now() - timedelta(days=90)
    memory.db.query(EpisodicMemory).filter(
        EpisodicMemory.created_at < cutoff
    ).delete()
```

---

## Network Security

### Firewall Configuration

Configure firewalls to restrict access:

```bash
# UFW (Ubuntu)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 8000/tcp  # Dashboard port
sudo ufw enable
```

```yaml
# AWS Security Group
Resources:
  SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Cognitive Engine Security Group
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: your.ip.address/32
        - IpProtocol: tcp
          FromPort: 8000
          ToPort: 8000
          CidrIp: your.network/24
```

### TLS/SSL Configuration

Use valid SSL certificates:

```python
# FastAPI with HTTPS
from fastapi import FastAPI
import uvicorn

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="path/to/key.pem",
        ssl_certfile="path/to/cert.pem"
    )
```

### Rate Limiting

Implement rate limiting to prevent abuse:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/query")
@limiter.limit("10/minute")
async def query(request: Request):
    return {"result": "response"}
```

### VPN/Private Networks

Deploy in private networks:

```yaml
# VPC configuration
Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      
  PrivateSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
```

---

## Application Security

### Authentication

Implement authentication for web interfaces:

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != os.environ.get('API_TOKEN'):
        raise HTTPException(status_code=403, detail="Invalid token")
    return token

@app.post("/query")
async def query(token: str = Depends(verify_token)):
    return {"result": "response"}
```

### Authorization

Implement role-based access control:

```python
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    READONLY = "readonly"

def check_permission(required_role: Role):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user.role != required_role and user.role != Role.ADMIN:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator
```

### Secure Dependencies

Keep dependencies updated:

```bash
# Check for vulnerabilities
pip install safety
safety check

# Update dependencies
pip install --upgrade -r requirements.txt

# Use pip-audit
pip install pip-audit
pip-audit
```

Use a requirements file with pinned versions:

```txt
# requirements.txt
openai==1.3.0
anthropic==0.7.0
pydantic==2.0.0
fastapi==0.100.0
```

### Code Security

Use static analysis tools:

```bash
# Bandit - Python security linter
pip install bandit
bandit -r cognitive_engine/

# Semgrep - semantic code analysis
pip install semgrep
semgrep --config=auto cognitive_engine/
```

### Logging Security

Don't log sensitive information:

```python
import logging

logger = logging.getLogger(__name__)

def process_query(query):
    # Don't log the full query if it contains sensitive data
    safe_query = sanitize_for_logging(query)
    logger.info(f"Processing query: {safe_query[:50]}...")
```

---

## Agent Security

### Goal Validation

Validate agent goals to prevent dangerous actions:

```python
class GoalValidator:
    DANGEROUS_KEYWORDS = ['delete', 'destroy', 'format', 'erase', 'hack']
    
    def validate(self, goal: str) -> bool:
        goal_lower = goal.lower()
        
        # Check for dangerous keywords
        for keyword in self.DANGEROUS_KEYWORDS:
            if keyword in goal_lower:
                return False
        
        # Check for system commands
        if goal_lower.startswith(('sudo', 'rm ', 'dd ')):
            return False
        
        # Check for external access attempts
        if 'ssh' in goal_lower or 'ftp' in goal_lower:
            return False
        
        return True

validator = GoalValidator()
if not validator.validate(user_goal):
    raise ValueError("Goal rejected for security reasons")
```

### Tool Restrictions

Restrict which tools agents can use:

```python
class ToolRegistry:
    SAFE_TOOLS = ['web_search', 'code_exec']
    DANGEROUS_TOOLS = ['file_delete', 'system_command']
    
    def get_tool(self, tool_name: str, user_role: str):
        if user_role != 'admin' and tool_name in self.DANGEROUS_TOOLS:
            raise PermissionError(f"Tool {tool_name} not allowed for role {user_role}")
        
        if tool_name not in self.SAFE_TOOLS + self.DANGEROUS_TOOLS:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        return self.tools[tool_name]
```

### Sandbox Execution

Execute code in sandboxed environment:

```python
import docker

class SandboxedExecutor:
    def execute_code(self, code: str):
        client = docker.from_env()
        
        # Run in isolated container
        container = client.containers.run(
            image='python:3.10-slim',
            command=['python', '-c', code],
            network_disabled=True,
            mem_limit='128m',
            cpu_quota=50000,
            runtime='runsc',  # gVisor for additional isolation
            remove=True,
            stdout=True,
            stderr=True
        )
        
        return container.decode('utf-8')
```

### Step Limits

Enforce step limits to prevent infinite loops:

```python
class Agent:
    def __init__(self, max_steps=100):
        self.max_steps = max_steps
        self.step_count = 0
    
    def run(self, goal: str):
        while not self.goal_achieved and self.step_count < self.max_steps:
            self.step_count += 1
            self.execute_step()
        
        if self.step_count >= self.max_steps:
            raise RuntimeError("Maximum steps exceeded")
```

### Memory Control

Control agent memory to prevent accumulation:

```python
class AgentMemory:
    MAX_MEMORY_ENTRIES = 1000
    
    def add_entry(self, entry):
        if len(self.memory) >= self.MAX_MEMORY_ENTRIES:
            # Remove oldest entries
            self.memory = self.memory[-(self.MAX_MEMORY_ENTRIES // 2):]
        
        self.memory.append(entry)
```

---

## Memory Security

### Memory Encryption

Encrypt sensitive memory entries:

```python
from cryptography.fernet import Fernet

class SecureMemory:
    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)
    
    def store(self, key, value):
        if self.is_sensitive(value):
            encrypted = self.cipher.encrypt(value.encode())
            self.db[key] = encrypted
        else:
            self.db[key] = value
    
    def retrieve(self, key):
        value = self.db[key]
        if isinstance(value, bytes):
            return self.cipher.decrypt(value).decode()
        return value
    
    def is_sensitive(self, value):
        # Check for PII, passwords, etc.
        sensitive_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{16}\b',  # Credit card
            r'password',
            r'token'
        ]
        return any(re.search(pattern, value, re.I) for pattern in sensitive_patterns)
```

### Memory Access Control

Control who can access memory:

```python
class MemoryAccessControl:
    def __init__(self):
        self.acl = {}  # access control list
    
    def grant_access(self, user_id, permissions):
        self.acl[user_id] = permissions
    
    def check_access(self, user_id, operation, data):
        if user_id not in self.acl:
            return False
        
        permissions = self.acl[user_id]
        if operation not in permissions:
            return False
        
        # Check data-level permissions
        if data.get('sensitivity', 'public') == 'confidential':
            return 'read_confidential' in permissions
        
        return True
```

### Memory Purging

Implement secure memory deletion:

```python
import hashlib
import os

def secure_delete(file_path):
    """Securely delete file by overwriting."""
    file_size = os.path.getsize(file_path)
    
    # Overwrite with random data multiple times
    with open(file_path, 'wb') as f:
        for _ in range(3):
            f.write(os.urandom(file_size))
            f.flush()
            os.fsync(f.fileno())
    
    # Delete file
    os.remove(file_path)
```

---

## Deployment Security

### Container Security

Secure Docker containers:

```dockerfile
# Use minimal base image
FROM python:3.10-slim

# Run as non-root user
RUN useradd -m -u 1000 cognitive_engine
USER cognitive_engine

# Use read-only filesystem
# Add --read-only flag to docker run

# Drop capabilities
# Add --cap-drop=ALL --cap-add=NET_BIND_SERVICE to docker run

# Use security options
# docker run --security-opt=no-new-privileges
```

### Kubernetes Security

Configure pod security:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cognitive-engine
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  containers:
  - name: cognitive-engine
    image: cognitive-engine:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
```

### Infrastructure Security

Use secure infrastructure configurations:

```yaml
# AWS IAM policy with least privilege
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

### Secrets Rotation

Automate secret rotation:

```python
import boto3
import time

class SecretRotator:
    def __init__(self, secret_name):
        self.client = boto3.client('secretsmanager')
        self.secret_name = secret_name
    
    def rotate_secret(self):
        # Generate new secret
        new_secret = self.generate_new_secret()
        
        # Update secret
        self.client.update_secret(
            SecretId=self.secret_name,
            SecretString=new_secret
        )
        
        # Wait for propagation
        time.sleep(30)
        
        # Test new secret
        if not self.test_secret(new_secret):
            # Rollback
            self.rollback_secret()
            raise RuntimeError("Secret rotation failed")
```

---

## Compliance

### GDPR Compliance

For EU data protection:

```python
class GDPRCompliance:
    def __init__(self):
        self.consent_manager = ConsentManager()
    
    def process_user_data(self, user_id, data):
        # Check consent
        if not self.consent_manager.has_consent(user_id):
            raise PermissionError("No consent for data processing")
        
        # Process with data minimization
        minimized_data = self.minimize_data(data)
        
        return self.process(minimized_data)
    
    def right_to_erasure(self, user_id):
        # Delete all user data
        self.delete_user_data(user_id)
        self.delete_user_memory(user_id)
        self.delete_user_logs(user_id)
```

### HIPAA Compliance

For healthcare data:

```python
class HIPAACompliance:
    def __init__(self):
        self.audit_logger = AuditLogger()
    
    def process_phi(self, data):
        # Log all access
        self.audit_logger.log_access(data)
        
        # Encrypt PHI
        encrypted = self.encrypt_phi(data)
        
        # Process
        result = self.process(encrypted)
        
        # Log outcome
        self.audit_logger.log_outcome(result)
        
        return result
```

### SOC 2 Compliance

For security controls:

```python
class SOC2Controls:
    def __init__(self):
        self.controls = {
            'access_control': self.enforce_access_control,
            'encryption': self.enforce_encryption,
            'monitoring': self.enable_monitoring,
            'change_management': self.track_changes
        }
    
    def audit_controls(self):
        report = {}
        for control_name, control_func in self.controls.items():
            report[control_name] = control_func()
        return report
```

---

## Security Auditing

### Logging Security Events

Log security-relevant events:

```python
import logging
from datetime import datetime

security_logger = logging.getLogger('security')

def log_security_event(event_type, details):
    security_logger.info({
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'details': details,
        'source': 'cognitive-engine'
    })

# Usage
log_security_event('AUTHENTICATION_SUCCESS', {
    'user_id': 'user123',
    'ip_address': '192.168.1.1'
})
```

### Intrusion Detection

Implement basic intrusion detection:

```python
class IntrusionDetector:
    def __init__(self):
        self.failed_attempts = {}
        self.blocked_ips = set()
    
    def check_failed_login(self, ip_address):
        if ip_address in self.failed_attempts:
            self.failed_attempts[ip_address] += 1
        else:
            self.failed_attempts[ip_address] = 1
        
        if self.failed_attempts[ip_address] >= 5:
            self.blocked_ips.add(ip_address)
            log_security_event('IP_BLOCKED', {'ip': ip_address})
    
    def is_ip_blocked(self, ip_address):
        return ip_address in self.blocked_ips
```

### Security Monitoring

Monitor security metrics:

```python
from prometheus_client import Counter, Histogram

security_metrics = {
    'failed_auth_attempts': Counter('failed_auth_attempts_total'),
    'api_key_errors': Counter('api_key_errors_total'),
    'suspicious_queries': Counter('suspicious_queries_total'),
    'response_time': Histogram('response_time_seconds')
}

def record_security_metric(metric_name, value=1):
    if metric_name in security_metrics:
        security_metrics[metric_name].inc(value)
```

### Regular Security Audits

Schedule regular security audits:

```python
import schedule
import time

def security_audit():
    """Run security audit checks."""
    print("Running security audit...")
    
    # Check for exposed API keys
    check_for_exposed_keys()
    
    # Review access logs
    review_access_logs()
    
    # Check dependency vulnerabilities
    check_dependencies()
    
    # Review user permissions
    review_permissions()
    
    print("Security audit complete")

# Schedule weekly audit
schedule.every().week.do(security_audit)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Security Best Practices Summary

### Do's

- ✅ Use environment variables for secrets
- ✅ Encrypt data at rest and in transit
- ✅ Implement authentication and authorization
- ✅ Validate all inputs
- ✅ Keep dependencies updated
- ✅ Use least privilege access
- ✅ Log security events
- ✅ Regular security audits
- ✅ Use secure coding practices
- ✅ Implement rate limiting

### Don'ts

- ❌ Commit secrets to version control
- ❌ Use default credentials
- ❌ Disable security features
- ❌ Ignore security warnings
- ❌ Use outdated dependencies
- ❌ Expose unnecessary ports
- ❌ Log sensitive information
- ❌ Skip input validation
- ❌ Run as root/admin
- ❌ Disable encryption

---

## Incident Response

### Security Incident Procedure

1. **Detect**
   - Monitor security logs
   - Set up alerts
   - Regular security scans

2. **Contain**
   - Isolate affected systems
   - Block malicious IPs
   - Revoke compromised credentials

3. **Eradicate**
   - Remove malware/vulnerabilities
   - Patch security holes
   - Clean compromised data

4. **Recover**
   - Restore from clean backups
   - Verify system integrity
   - Monitor for recurrence

5. **Learn**
   - Document incident
   - Update procedures
   - Train team

### Incident Reporting

Report security incidents:

```python
def report_incident(incident_details):
    """Report security incident."""
    import smtplib
    from email.mime.text import MIMEText
    
    msg = MIMEText(f"Security Incident:\n\n{incident_details}")
    msg['Subject'] = 'Security Incident Alert'
    msg['From'] = 'security@cognitiveengine.org'
    msg['To'] = 'security-team@cognitiveengine.org'
    
    # Send to security team
    # Implementation depends on your email system
```

---

## Support

For security issues:
- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- Report security vulnerabilities responsibly
- Do not disclose publicly before fix
