#!/bin/sh
export INFISICAL_TOKEN=$(cat /run/secrets/infisical_token)
cd /run/secrets
infisical run --path="/Sphere/backend" -- sh -c '
  cd /app &&
  
  # Test PostgreSQL connection with retry
  echo "Testing connection to PostgreSQL server at $DB_HOST:$DB_PORT..."
  retries=5
  delay=2
  attempt=1
  while [ $attempt -le $retries ]; do
    if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; then
      echo "PostgreSQL server is ready!"
      break
    fi
    echo "Attempt $attempt/$retries: Waiting for PostgreSQL server to be ready..."
    sleep $delay
    attempt=$((attempt + 1))
    if [ $attempt -gt $retries ]; then
      echo "Error: PostgreSQL server not available after $retries attempts. Exiting..." >&2
      exit 1
    fi
  done

  # Start Celery worker
  echo "Starting Celery worker..."
  celery -A backend worker --loglevel=info --uid nobody
'