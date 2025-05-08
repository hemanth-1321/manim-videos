# Use a slim base to reduce image size
FROM python:3.12-slim


# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libcairo2-dev \
    libpango1.0-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies early for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Manim
RUN pip install --no-cache-dir manim

# Copy project files
COPY ./prisma ./prisma
COPY . .

# Generate Prisma client
RUN prisma generate

# Expose port
EXPOSE 8080

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
