#!/bin/bash

# Attendre que PostgreSQL soit prêt
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Attendre que HDFS soit prêt
echo "Waiting for HDFS..."
while ! hdfs dfsadmin -safemode get | grep -q "Safe mode is OFF"; do
  sleep 5
done
echo "HDFS is ready!"

# Initialiser la base de données si nécessaire
if [ ! -f "/opt/airflow/airflow.db" ]; then
    echo "Initializing Airflow database..."
    airflow db init
    airflow users create \
        --username airflow \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com \
        --password airflow
fi

# Démarrer le webserver en arrière-plan
echo "Starting Airflow webserver..."
airflow webserver --port 8080 &

# Démarrer le scheduler
echo "Starting Airflow scheduler..."
airflow scheduler 