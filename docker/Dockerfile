FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git curl && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY *.py .
COPY README.md .

# Create data directory
RUN mkdir -p /data

# Set environment variable for data directory
ENV DATA_DIR=/data

# Create non-root user for security
RUN useradd -m -u 1000 downloader && \
    chown -R downloader:downloader /app /data

# Switch to non-root user
USER downloader

# Default command
CMD ["python", "download_all.py", "--dir", "/data/cybersecurity_datasets"]
