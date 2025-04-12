# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY knowledge/ ./knowledge/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Set environment variables
ENV PORT=8080
ENV HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "src.my_crew.app:app", "--host", "0.0.0.0", "--port", "8080"]
