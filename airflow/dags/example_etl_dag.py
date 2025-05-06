from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import subprocess
import json
import time

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_data():
    """Tâche 1: Extraction de données météo depuis une API et stockage dans HDFS"""
    # Configuration WebHDFS
    webhdfs_url = "http://172.20.0.3:9870/webhdfs/v1"
    user = "airflow"
    
    # Créer le répertoire de données si nécessaire
    data_dir = "/user/airflow/weather_data"
    mkdir_url = f"{webhdfs_url}{data_dir}?op=MKDIRS&user.name={user}"
    requests.put(mkdir_url)
    
    # Simuler des données météo (dans un cas réel, on appellerait une API)
    weather_data = {
        "timestamp": datetime.now().isoformat(),
        "temperature": 22.5,
        "humidity": 65,
        "pressure": 1013,
        "wind_speed": 12.3,
        "city": "Paris"
    }
    
    # Sauvegarder dans HDFS
    filename = f"{data_dir}/weather_{int(time.time())}.json"
    create_url = f"{webhdfs_url}{filename}?op=CREATE&user.name={user}"
    response = requests.put(create_url, data=json.dumps(weather_data))
    response.raise_for_status()
    
    print(f"Données extraites et sauvegardées dans {filename}")
    return filename

def transform_data(hdfs_file):
    """Tâche 2: Transformation des données et création d'une table Hive"""
    # Créer la base de données si nécessaire
    create_db_cmd = """
    beeline -u jdbc:hive2://hive-server:10000 -n airflow -e "
    CREATE DATABASE IF NOT EXISTS weather_db;
    USE weather_db;
    "
    """
    subprocess.run(create_db_cmd, shell=True, check=True)
    
    # Créer la table externe pointant vers les données HDFS
    create_table_cmd = f"""
    beeline -u jdbc:hive2://hive-server:10000 -n airflow -e "
    USE weather_db;
    CREATE EXTERNAL TABLE IF NOT EXISTS weather_data (
        timestamp STRING,
        temperature DOUBLE,
        humidity INT,
        pressure INT,
        wind_speed DOUBLE,
        city STRING
    )
    ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
    LOCATION '{hdfs_file}';
    "
    """
    subprocess.run(create_table_cmd, shell=True, check=True)
    
    print("Table Hive créée avec succès")
    return "weather_db.weather_data"

def load_data(hive_table):
    """Tâche 3: Chargement des données transformées et création d'une vue agrégée"""
    # Créer une vue agrégée des données
    create_view_cmd = f"""
    beeline -u jdbc:hive2://hive-server:10000 -n airflow -e "
    USE weather_db;
    CREATE OR REPLACE VIEW weather_summary AS
    SELECT 
        city,
        AVG(temperature) as avg_temperature,
        AVG(humidity) as avg_humidity,
        AVG(pressure) as avg_pressure,
        AVG(wind_speed) as avg_wind_speed,
        COUNT(*) as record_count
    FROM {hive_table}
    GROUP BY city;
    "
    """
    subprocess.run(create_view_cmd, shell=True, check=True)
    
    # Afficher les résultats
    show_results_cmd = """
    beeline -u jdbc:hive2://hive-server:10000 -n airflow -e "
    USE weather_db;
    SELECT * FROM weather_summary;
    "
    """
    result = subprocess.run(show_results_cmd, shell=True, capture_output=True, text=True)
    print("\nRésultats de l'agrégation:")
    print(result.stdout)
    
    return "Vue agrégée créée avec succès"

with DAG(
    'example_etl_dag',
    default_args=default_args,
    description='Exemple de DAG ETL avec HDFS et Hive',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example', 'etl', 'hdfs', 'hive'],
) as dag:

    extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_kwargs={'hdfs_file': "{{ ti.xcom_pull(task_ids='extract_data') }}"},
    )

    load = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        op_kwargs={'hive_table': "{{ ti.xcom_pull(task_ids='transform_data') }}"},
    )

    extract >> transform >> load 