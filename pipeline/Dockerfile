# Dockerfile for Prefect 3 serverless deployment
FROM python:3.12-slim

# -----------------------------
# 1. Install system dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Optional: GDAL env vars (usually needed only when compiling, can skip for prebuilt wheels)
# ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
# ENV C_INCLUDE_PATH=/usr/include/gdal

# -----------------------------
# 2. Set working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# 3. Copy requirements
# -----------------------------
COPY pipeline/requirements.txt ./requirements.txt

# -----------------------------
# 4. Install Python dependencies
# -----------------------------
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# -----------------------------
# 5. Copy project files
# -----------------------------
COPY . .

# -----------------------------
# 6. Default command (Prefect overrides)
# -----------------------------
CMD ["python", "pipeline/main.py"]