#!/usr/bin/env bash
set -e

# Fallback si jamais la variable ne passe pas
PG_HOST=${POSTGRES_HOST:-postgres}
PG_PORT=${POSTGRES_PORT:-5432}

echo "⏳ Waiting for PostgreSQL at ${PG_HOST}:${PG_PORT}…"
until nc -z "$PG_HOST" "$PG_PORT"; do
  sleep 1
done
echo "✅ PostgreSQL is up!"

# Installation des providers avec les contraintes
echo "📦 Installing Airflow providers..."
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-2.7.1/constraints-3.8.txt"
pip install --no-cache-dir \
    --constraint "${CONSTRAINT_URL}" \
    apache-airflow-providers-apache-hdfs \
    apache-airflow-providers-apache-hive \
    requests-kerberos \
    gssapi \
    'hdfs[avro,dataframe]>=2.5.4'

# Initialisation de la BDD Airflow
echo "📦 Initializing Airflow database..."
airflow db init

# Puis votre import de connexions
echo "🔌 Importing Airflow connections..."
python /opt/airflow/scripts/import_connections.py

# Enfin on démarre le webserver
echo "🚀 Starting Airflow webserver..."
exec airflow "$@" 