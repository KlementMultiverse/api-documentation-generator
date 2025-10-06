FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make analyzer executable
RUN chmod +x analyzer.py

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "print('healthy')" || exit 1

# Default command: show help
CMD ["python", "analyzer.py", "--help"]
