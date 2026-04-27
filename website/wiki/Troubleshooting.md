# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Cognitive Engine.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Issues](#configuration-issues)
- [Runtime Issues](#runtime-issues)
- [Performance Issues](#performance-issues)
- [Memory Issues](#memory-issues)
- [LLM API Issues](#llm-api-issues)
- [Dashboard Issues](#dashboard-issues)
- [Agent Issues](#agent-issues)
- [Learning System Issues](#learning-system-issues)
- [Database Issues](#database-issues)
- [Getting Help](#getting-help)

---

## Installation Issues

### Python Version Incompatible

**Symptom**: `SyntaxError` or module import errors after installation

**Cause**: Python version too old or incompatible

**Solution**:
```bash
# Check Python version
python --version

# Install Python 3.9 or higher
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv

# On macOS with Homebrew
brew install python@3.10

# On Windows
# Download from https://www.python.org/downloads/
```

### Dependencies Fail to Install

**Symptom**: `pip install` fails with build errors

**Cause**: Missing system dependencies or incompatible versions

**Solution**:
```bash
# Update pip
pip install --upgrade pip

# Install system dependencies
# Ubuntu/Debian
sudo apt-get install build-essential python3-dev

# macOS
xcode-select --install

# Try installing with specific versions
pip install -r requirements.txt --no-cache-dir

# If still failing, try:
pip install --upgrade setuptools wheel
pip install -r requirements.txt
```

### Virtual Environment Issues

**Symptom**: Cannot activate virtual environment or modules not found

**Cause**: Incorrect virtual environment setup or activation

**Solution**:
```bash
# Remove existing venv
rm -rf venv

# Create new venv
python3 -m venv venv

# Activate correctly
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# Verify activation
which python  # Should show venv path
```

---

## Configuration Issues

### API Key Not Found

**Symptom**: `API key not found` or `No LLM API key configured`

**Cause**: Missing or incorrect environment variables

**Solution**:
```bash
# Check .env file exists
ls -la .env

# Create from example if missing
cp .env.example .env

# Edit .env and add keys
nano .env

# Verify keys are set
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# If using Docker, pass environment variables
docker run -e OPENAI_API_KEY=your_key ...
```

### Configuration Not Loading

**Symptom**: Default values used instead of configured values

**Cause**: `.env` file not in correct location or format incorrect

**Solution**:
```bash
# Ensure .env is in project root
pwd  # Should be cognitive_engine directory
ls .env

# Check format (no spaces around =)
# Correct: KEY=value
# Wrong: KEY = value

# Reload environment
source .env  # Linux/macOS
# or restart application

# Check for typos in variable names
# Should match exactly: OPENAI_API_KEY not OPENAIKEY
```

### Port Already in Use

**Symptom**: `Address already in use` or `Port 8000 already in use`

**Cause**: Dashboard port or another service using the port

**Solution**:
```bash
# Find process using port
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # Linux/macOS
taskkill /PID <PID> /F  # Windows

# Or change port in .env
DASHBOARD_PORT=8001
```

---

## Runtime Issues

### Engine Won't Start

**Symptom**: Application crashes immediately on startup

**Cause**: Missing dependencies, configuration errors, or import errors

**Solution**:
```bash
# Check error message in logs
tail -f cognitive_engine.log

# Run in verbose mode
LOG_LEVEL=DEBUG python run.py

# Check imports
python -c "from core.engine import CognitiveEngine"

# Verify all dependencies installed
pip list | grep -E "(openai|anthropic|pydantic|fastapi)"

# Reinstall if needed
pip install --force-reinstall -r requirements.txt
```

### Import Errors

**Symptom**: `ModuleNotFoundError: No module named 'xxx'`

**Cause**: Module not installed or Python path issues

**Solution**:
```bash
# Ensure virtual environment activated
which python

# Install missing module
pip install <module_name>

# Check PYTHONPATH
echo $PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/cognitive_engine"

# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Process Hangs

**Symptom**: Application becomes unresponsive or hangs

**Cause**: Infinite loop, blocking operation, or deadlock

**Solution**:
```bash
# Check process status
ps aux | grep python

# Get stack trace (Linux)
kill -QUIT <PID>

# Check logs for loops
tail -f cognitive_engine.log

# Reduce iteration limits in config
MIN_ITERATIONS=1
MAX_ITERATIONS=10

# Enable debug logging
LOG_LEVEL=DEBUG
```

---

## Performance Issues

### Slow Response Times

**Symptom**: Queries take too long to complete

**Cause**: High iteration count, slow LLM, or inefficient code

**Solution**:
```bash
# Reduce iteration limits
MIN_ITERATIONS=1
MAX_ITERATIONS=20

# Use faster LLM provider
DEFAULT_LLM_PROVIDER=openai  # Generally faster than anthropic

# Enable caching if available
ENABLE_CACHING=true

# Check system resources
htop  # Linux/macOS
Task Manager  # Windows

# Profile the application
python -m cProfile -o profile.stats run.py
python -m pstats profile.stats
```

### High CPU Usage

**Symptom**: CPU usage near 100%

**Cause**: Intensive computation or infinite loop

**Solution**:
```bash
# Check what's using CPU
top -p <PID>

# Reduce cognitive iterations
MAX_ITERATIONS=30

# Disable expensive features
ENABLE_LEARNING=false
ENABLE_PROMPT_EVOLUTION=false

# Add rate limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=60
```

### High Memory Usage

**Symptom**: Memory usage grows continuously

**Cause**: Memory leak or unbounded memory growth

**Solution**:
```bash
# Check memory usage
free -h  # Linux
vm_stat  # macOS

# Limit memory size
MAX_MEMORY_SIZE=5000

# Enable memory cleanup
ENABLE_MEMORY_CLEANUP=true

# Clear memory periodically
python run.py cleanup

# Check for memory leaks
pip install memory_profiler
python -m memory_profiler run.py
```

---

## Memory Issues

### Database Locked

**Symptom**: `SQLite database is locked`

**Cause**: Multiple processes accessing database simultaneously

**Solution**:
```bash
# Check for other processes
ps aux | grep python

# Stop other instances
pkill -f "python run.py"

# Use WAL mode for better concurrency
# Add to database initialization
PRAGMA journal_mode=WAL;

# Or use PostgreSQL for production
DATABASE_URL=postgresql://user:pass@localhost/db
```

### Memory Not Persisting

**Symptom**: Memory lost after restart

**Cause**: Database path incorrect or permissions issue

**Solution**:
```bash
# Check database file exists
ls -la cognitive_engine.db

# Check permissions
chmod 644 cognitive_engine.db

# Verify path in config
MEMORY_DB_PATH=cognitive_engine.db

# Use absolute path
MEMORY_DB_PATH=/full/path/to/cognitive_engine.db

# Check disk space
df -h
```

### Memory Corruption

**Symptom**: Strange data in memory or crashes

**Cause**: Database corruption or concurrent access

**Solution**:
```bash
# Backup current database
cp cognitive_engine.db cognitive_engine.db.backup

# Try to repair
sqlite3 cognitive_engine.db "PRAGMA integrity_check;"

# If corrupted, restore from backup
cp cognitive_engine.db.backup cognitive_engine.db

# Start fresh if needed
rm cognitive_engine.db
python run.py  # Will recreate
```

---

## LLM API Issues

### API Key Invalid

**Symptom**: `Invalid API key` or `401 Unauthorized`

**Cause**: Incorrect API key or key revoked

**Solution**:
```bash
# Verify key is correct
echo $OPENAI_API_KEY

# Regenerate key from provider
# OpenAI: https://platform.openai.com/api-keys
# Anthropic: https://console.anthropic.com/

# Update .env file
nano .env

# Restart application
```

### Rate Limit Exceeded

**Symptom**: `Rate limit exceeded` or `429 Too Many Requests`

**Cause**: Too many API requests in short time

**Solution**:
```bash
# Implement exponential backoff
# Already handled in client, but can tune
RETRY_DELAY=1
MAX_RETRIES=3

# Reduce request frequency
# Add delay between requests
REQUEST_DELAY=0.5

# Upgrade API plan
# OpenAI: https://platform.openai.com/account/billing
# Anthropic: https://console.anthropic.com/settings/billing

# Use caching
ENABLE_RESPONSE_CACHE=true
CACHE_TTL=3600
```

### API Timeout

**Symptom**: Request times out after long wait

**Cause**: Network issues or slow LLM response

**Solution**:
```bash
# Increase timeout
LLM_TIMEOUT=60

# Check network connectivity
ping api.openai.com
ping api.anthropic.com

# Use faster model
DEFAULT_MODEL=gpt-3.5-turbo  # Instead of gpt-4

# Check provider status
# OpenAI: https://status.openai.com/
# Anthropic: https://status.anthropic.com/
```

### Insufficient Quota

**Symptom**: `Insufficient quota` or billing error

**Cause**: API quota exceeded or billing issue

**Solution**:
```bash
# Check quota/billing
# OpenAI: https://platform.openai.com/account/usage
# Anthropic: https://console.anthropic.com/settings/billing

# Add credits or upgrade plan

# Monitor usage
python run.py monitor-usage
```

---

## Dashboard Issues

### Dashboard Not Accessible

**Symptom**: Cannot access dashboard at http://localhost:8000

**Cause**: Dashboard not enabled or wrong port

**Solution**:
```bash
# Check dashboard enabled
ENABLE_DASHBOARD=true

# Check correct port
DASHBOARD_PORT=8000

# Verify server running
ps aux | grep "python run.py"

# Check firewall
sudo ufw allow 8000  # Linux
# Windows Firewall settings

# Try different port
DASHBOARD_PORT=8080
```

### WebSocket Connection Failed

**Symptom**: `WebSocket connection failed` in browser console

**Cause**: WebSocket not enabled or blocked

**Solution**:
```bash
# Check WebSocket enabled
ENABLE_WEBSOCKET=true

# Check browser console for errors
# F12 → Console tab

# Try different browser
# Chrome, Firefox, Safari

# Check for proxy issues
# Disable VPN or proxy temporarily

# Verify WebSocket URL
ws://localhost:8000/ws
```

### Dashboard Not Updating

**Symptom**: Dashboard shows stale data or no updates

**Cause**: Event stream not working or client disconnected

**Solution**:
```bash
# Check server logs
tail -f cognitive_engine.log

# Refresh browser page
# Ctrl+Shift+R (hard refresh)

# Check WebSocket connection
# Browser console → Network tab → WS

# Restart dashboard
python run.py dashboard
```

---

## Agent Issues

### Agent Not Responding

**Symptom**: Agent accepts goal but doesn't produce output

**Cause**: Goal validation failing or tool error

**Solution**:
```bash
# Check goal validation
AGENT_GOAL_VALIDATION=false  # Disable temporarily

# Check tool availability
python run.py list-tools

# Check agent logs
tail -f cognitive_engine.log | grep agent

# Try simple goal
python run.py agent "What is 2+2?"
```

### Tool Execution Fails

**Symptom**: Agent tool calls fail with errors

**Cause**: Tool not registered or invalid parameters

**Solution**:
```bash
# Check tool registry
python run.py check-tools

# Verify tool permissions
TOOL_PERMISSIONS=permissive

# Check tool-specific configuration
# e.g., for web search
WEB_SEARCH_API_KEY=your_key

# Test tool directly
python -c "from tools.web_search import WebSearchTool; tool = WebSearchTool(); print(tool.search('test'))"
```

### Agent Loops

**Symptom**: Agent repeats same actions indefinitely

**Cause**: Missing step limit or goal unclear

**Solution**:
```bash
# Set step limit
AGENT_STEP_LIMIT=50

# Clarify goal
# Be more specific in goal description

# Enable goal validation
AGENT_GOAL_VALIDATION=true

# Check logs for patterns
tail -f cognitive_engine.log
```

---

## Learning System Issues

### Patterns Not Extracting

**Symptom**: Learning system not finding patterns

**Cause**: Insufficient data or threshold too high

**Solution**:
```bash
# Check learning enabled
ENABLE_LEARNING=true

# Lower pattern threshold
PATTERN_THRESHOLD=3

# Check memory has data
python run.py check-memory

# Force pattern extraction
python run.py extract-patterns
```

### Rules Not Applying

**Symptom**: Learned rules not being used

**Cause**: Rules not synthesized or effectiveness too low

**Solution**:
```bash
# Check rule effectiveness threshold
RULE_EFFECTIVENESS_THRESHOLD=0.5

# Force rule synthesis
python run.py synthesize-rules

# Check rule memory
python run.py list-rules

# Manually apply rules
python run.py apply-rules
```

### Learning Too Slow

**Symptom**: Learning operations take too long

**Cause**: Too much data or inefficient extraction

**Solution**:
```bash
# Increase learning interval
LEARNING_INTERVAL=500

# Reduce memory size
MAX_MEMORY_SIZE=5000

# Disable learning temporarily
ENABLE_LEARNING=false

# Clear old memory
python run.py clear-old-memory
```

---

## Database Issues

### Database Connection Failed

**Symptom**: Cannot connect to database

**Cause**: Database not running or wrong credentials

**Solution**:
```bash
# Check database file exists
ls -la cognitive_engine.db

# Check permissions
chmod 644 cognitive_engine.db

# Try with absolute path
MEMORY_DB_PATH=/full/path/to/cognitive_engine.db

# Recreate database
rm cognitive_engine.db
python run.py
```

### Query Performance Slow

**Symptom**: Database queries take too long

**Cause**: Missing indexes or large dataset

**Solution**:
```bash
# Add indexes
# In database initialization
CREATE INDEX IF NOT EXISTS idx_timestamp ON episodic_memory(timestamp);

# Vacuum database
sqlite3 cognitive_engine.db "VACUUM;"

# Reduce dataset size
MAX_MEMORY_SIZE=10000

# Consider PostgreSQL for production
DATABASE_URL=postgresql://user:pass@localhost/db
```

### Database File Too Large

**Symptom**: Database file growing too large

**Cause**: Unbounded memory growth

**Solution**:
```bash
# Set memory limit
MAX_MEMORY_SIZE=10000

# Enable retention policy
MEMORY_RETENTION_DAYS=90

# Clear old data
python run.py clear-old-memory

# Backup and recreate
cp cognitive_engine.db backup.db
rm cognitive_engine.db
python run.py
```

---

## Getting Help

### Diagnostic Information

Before seeking help, gather diagnostic information:

```bash
# System information
python --version
pip list
uname -a  # Linux/macOS
systeminfo  # Windows

# Configuration
cat .env

# Logs (last 100 lines)
tail -100 cognitive_engine.log

# Memory status
python run.py status

# Database check
sqlite3 cognitive_engine.db "PRAGMA integrity_check;"
```

### Log Files

Check log files for error messages:

```bash
# Main log
tail -f cognitive_engine.log

# Debug log
LOG_LEVEL=DEBUG python run.py 2>&1 | tee debug.log

# System logs
journalctl -u cognitive-engine  # systemd
/var/log/syslog  # Linux system log
```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Missing module | `pip install <module>` |
| `API key not found` | Missing API key | Set in `.env` |
| `Database locked` | Concurrent access | Use WAL mode or PostgreSQL |
| `Rate limit exceeded` | Too many requests | Implement backoff, upgrade plan |
| `Port already in use` | Port conflict | Change port or kill process |
| `Permission denied` | File permissions | `chmod 644 file` |
| `Out of memory` | Memory limit reached | Increase memory or reduce usage |

### Support Channels

- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- **GitHub Issues**: Check existing issues first
- **Documentation**: Review relevant wiki pages
- **Logs**: Always include log excerpts

### When Reporting Issues

Include:
1. Python version
2. Operating system
3. Error message (full traceback)
4. Configuration (sanitized)
5. Steps to reproduce
6. Expected vs actual behavior
7. Log excerpts (relevant sections)

### Debug Mode

Enable debug mode for more information:

```bash
# Set debug log level
LOG_LEVEL=DEBUG

# Enable verbose output
VERBOSE=true

# Run with Python debugger
python -m pdb run.py

# Or use breakpoint() in code
```

### Clean Slate

If all else fails, start fresh:

```bash
# Backup current state
cp -r cognitive_engine cognitive_engine.backup
cp .env .env.backup
cp cognitive_engine.db cognitive_engine.db.backup

# Remove virtual environment
rm -rf venv

# Remove database
rm cognitive_engine.db

# Remove logs
rm cognitive_engine.log

# Recreate everything
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Prevention

### Regular Maintenance

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Clear old memory
python run.py cleanup

# Backup database
cp cognitive_engine.db backup/cognitive_engine_$(date +%Y%m%d).db

# Check disk space
df -h

# Monitor logs
tail -f cognitive_engine.log
```

### Health Checks

```bash
# Run health check
python run.py health

# Check all components
python run.py check-all

# Test configuration
python run.py test-config
```

### Monitoring

Set up monitoring for:
- Error rates
- Response times
- Memory usage
- CPU usage
- Disk space
- API quota usage
