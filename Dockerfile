# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy only necessary files
COPY requirements.txt ./

# Install Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Now copy the actual app
COPY app/ ./app/

# Expose port for Streamlit
EXPOSE 80

# Start Streamlit
CMD ["streamlit", "run", "app/frontend_chat.py", "--server.port=80", "--server.enableCORS=false"]
