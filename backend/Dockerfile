FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl postgresql-client-15 && \
    curl -1sLf 'https://artifacts-cli.infisical.com/setup.deb.sh' | bash && \
    apt-get install -y infisical && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY . .
RUN chmod +x run.sh run-celery.sh run-celery-beat.sh

EXPOSE 8000
