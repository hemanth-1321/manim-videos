FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg\
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN pip install manim

COPY prisma ./prisma
COPY . .

RUN prisma generate

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]