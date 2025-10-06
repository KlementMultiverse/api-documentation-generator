# 🚀 Quick Start Guide

## For Complete Beginners

### What This Tool Does
This tool analyzes your application log files and uses AI to automatically find problems and suggest fixes. It's like having an expert DevOps engineer look at your logs and tell you exactly what went wrong.

---

## 3-Minute Quick Start

### Option 1: Try the Demo (No Setup)

```bash
# Clone the repo
git clone https://github.com/KlementMultiverse/api-documentation-generator.git
cd api-documentation-generator

# Run demo (uses Python 3)
python3 analyzer.py demo
```

You'll see:
- A sample log file analyzed
- AI-detected root cause
- Recommended fixes
- Prevention strategies

### Option 2: Analyze Your Own Logs

```bash
# Install dependencies (one time)
pip3 install rich requests pandas

# Analyze any log file
python3 analyzer.py analyze /path/to/your/app.log

# Save report to file
python3 analyzer.py analyze /path/to/your/app.log --output report.md
```

### Option 3: Use Docker (Everything Automated)

```bash
# Build and run
docker build -t log-analyzer .
docker run --rm log-analyzer python analyzer.py demo

# Analyze your own logs
docker run --rm -v $(pwd)/logs:/app/logs log-analyzer python analyzer.py analyze logs/your-file.log
```

---

## Real Example

Let's say your application crashed and you have this log:

```bash
# Create a test log file
cat > myapp.log << 'EOF'
2024-01-15 10:00:00 INFO: Application started
2024-01-15 10:00:01 INFO: Connected to database
2024-01-15 10:05:30 ERROR: Connection timeout to database
2024-01-15 10:05:31 ERROR: Failed to process user request
2024-01-15 10:05:32 ERROR: API returned 500
EOF

# Analyze it
python3 analyzer.py analyze myapp.log
```

**Output:**
```
🔍 Log Analysis Report

ROOT CAUSE: Database connection timeout - service is unreachable or slow

FIXES:
1. Check database server is running: systemctl status postgresql
2. Increase connection timeout in app config
3. Review database server logs for issues

PREVENTION: Add health checks, connection pooling, and retry logic
```

---

## Common Use Cases

### 1. My App Crashed in Production

```bash
# Export logs from your server
ssh user@server "tail -n 1000 /var/log/myapp.log" > crash.log

# Analyze locally
python3 analyzer.py analyze crash.log

# Get detailed report
python3 analyzer.py analyze crash.log --output crash-report.md
```

### 2. API is Slow - Find Why

```bash
# Analyze performance logs
python3 analyzer.py analyze api-performance.log

# Look for patterns in output:
# - Slow endpoints
# - Database query issues
# - N+1 query problems
```

### 3. Microservices Are Failing

```bash
# Analyze multiple service logs together
cat service1.log service2.log service3.log > combined.log
python3 analyzer.py analyze combined.log
```

---

## Using AI Features (Optional)

The tool works without AI, but for smarter analysis:

### Get Free AI API Key

1. Go to https://build.nvidia.com
2. Create free account
3. Get API key
4. Set environment variable:

```bash
export NVIDIA_API_KEY="nvapi-YOUR-KEY-HERE"
```

Now the tool will use AI for much better root cause analysis!

---

## Makefile Commands

If you're in the project directory:

```bash
make demo              # Run demo
make analyze FILE=app.log  # Analyze specific file
make test              # Run tests
make docker-run        # Run with Docker
```

---

## Troubleshooting

### "python: command not found"
Use `python3` instead of `python`

### "No module named 'rich'"
Install dependencies: `pip3 install rich requests pandas`

### "File not found"
Use full path: `python3 analyzer.py analyze /full/path/to/file.log`

### AI analysis says "fallback mode"
Set your NVIDIA_API_KEY or OPENAI_API_KEY environment variable

---

## Next Steps

1. ✅ Try the demo: `python3 analyzer.py demo`
2. ✅ Analyze your own logs
3. ✅ Get AI API key for smarter analysis
4. ✅ Integrate into your deployment pipeline
5. ✅ Star the repo if you find it useful!

---

## Getting Help

- 📖 Read the main [README.md](../README.md)
- 🐛 Report issues on [GitHub](https://github.com/KlementMultiverse/api-documentation-generator/issues)
- 💬 Connect on [LinkedIn](https://www.linkedin.com/in/klement-gunndu-601872351)

---

**Built with 🤖 Human-AI Collaboration**
