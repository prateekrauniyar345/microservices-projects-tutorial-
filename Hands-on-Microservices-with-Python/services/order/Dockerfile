FROM python:3.13-slim

WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY order_service.py .

# Expose port
EXPOSE 5010

# Run Flask when container starts (not during build)
# Start Flask application with auto-reload
CMD ["flask", "--app", "order_service", "run", "--host=0.0.0.0", "--port=5010", "--reload"]