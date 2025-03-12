FROM python:3.13-slim

WORKDIR /app

# Install system dependencies including C++ compiler
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "server.py"]