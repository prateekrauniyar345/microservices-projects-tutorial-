FROM python:3.13-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY user_service.py .

EXPOSE 5010

# Start Flask application
CMD ["flask", "--app", "user_service", "run", "--host=0.0.0.0", "--port=5010"]
