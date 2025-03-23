# Build stage
FROM ubuntu:22.04 AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    GDAL_SKIP=DODS \
    CPLUS_INCLUDE_PATH=/usr/include/gdal \
    C_INCLUDE_PATH=/usr/include/gdal \
    LC_ALL=C.UTF-8 \
    LC_CTYPE=C.UTF-8 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Install system dependencies
RUN apt-get update -qq && apt-get install -y -qq \
    git \
    ca-certificates \
    wget \
    make \
    bzip2 \
    g++ \
    build-essential \
    pkg-config \
    xmlsec1 \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    libpq-dev \
    python3-pip \
    gdal-bin \
    binutils \
    libproj-dev \
    libgdal-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*


# Create virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Upgrade pip
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements to leverage Docker cache
COPY indrz/requirements/base.txt /app/requirements/
COPY indrz/requirements/local.txt /app/requirements/

# Install Python dependencies
# required for libxmlsec1 to work with new security updates
RUN python3 -m pip install --upgrade pip setuptools

# Install Python module requirements
RUN pip install --no-cache-dir -r requirements/local.txt

# Final stage
FROM python:3.13.2-slim-bookworm AS final

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    GDAL_SKIP=DODS \
    PATH="/opt/venv/bin:$PATH" \
    LC_ALL=C.UTF-8 \
    LC_CTYPE=C.UTF-8

# Install runtime dependencies
RUN apt-get update -qq && apt-get install -y -qq \
    python3 \
    gdal-bin \
    libpq5 \
    postgresql-client \
    xmlsec1 \
    curl \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY indrz/ /app/
COPY devops/docker/local/indrz_api/entrypoint.sh /entrypoint.sh

# Set entrypoint permissions
RUN chmod +x /entrypoint.sh


# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000

ENTRYPOINT ["bash", "/entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
