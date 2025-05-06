FROM apache/airflow:2.7.1

USER root

# Installation des dépendances de base
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    net-tools \
    procps \
    iputils-ping \
    dnsutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copie du script de démarrage
COPY start-airflow.sh /start-airflow.sh
RUN chmod +x /start-airflow.sh

USER airflow

# Installation des providers Airflow (sans Kerberos)
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-hdfs[dataframe] \
    apache-airflow-providers-apache-hive \
    apache-airflow-providers-apache-spark \
    apache-airflow-providers-postgres

# Configuration d'Airflow
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__FERNET_KEY=''
ENV AIRFLOW__WEBSERVER__SECRET_KEY=''

# Point d'entrée
CMD ["/start-airflow.sh"] 