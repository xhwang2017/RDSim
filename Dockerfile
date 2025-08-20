# Use lightweight Python base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies: bash, curl, bcftools, plink2
RUN apt-get update && apt-get install -y \
    bash \
    build-essential \
    curl \
    wget \
    unzip \
    bcftools \
    && rm -rf /var/lib/apt/lists/*

# Install PLINK2
RUN wget https://s3.amazonaws.com/plink2-assets/plink2_linux_x86_64_latest.zip \
    && unzip plink2_linux_x86_64_latest.zip -d /usr/local/bin/ \
    && rm plink2_linux_x86_64_latest.zip

# Copy all scripts into container
COPY script/ /app/script/
COPY src/ /app/src/
COPY data/ /app/data/

# Install Python dependencies if requirements.txt exists
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt || true

# Make scripts executable
RUN chmod +x /app/script/RDSim.sh \
    && chmod +x /app/src/*.sh

# Default command (runs wrapper script)
CMD ["bash", "/app/script/RDSim.sh"]
