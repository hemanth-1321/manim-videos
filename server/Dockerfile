FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Prisma schema and other files needed
COPY prisma ./prisma
COPY . .

# Run Prisma generate
RUN prisma generate

EXPOSE 8080

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
