FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

RUN apt-get update && apt-get install -y texlive-full

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libcairo2-dev \
    libpango1.0-dev \
    texlive-full \
    ffmpeg\
    curl \
    git \
    && apt-get clean
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN pip install manim
COPY prisma ./prisma

COPY . .

RUN prisma generate

EXPOSE 8080

CMD ["fastapi", "run", "main.py", "--port", "8080"]
