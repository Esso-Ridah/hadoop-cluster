from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import os, tempfile, subprocess, requests
from urllib.parse import urljoin

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def download_movielens_data():
    """Télécharge les données MovieLens et les stocke temporairement"""
    # URL des données MovieLens (version 1M)
    base_url = "https://files.grouplens.org/datasets/movielens/ml-1m.zip"
    
    # Créer un dossier temporaire persistant pour ce run
    temp_dir = tempfile.mkdtemp(prefix="ml1m_")
    zip_path = os.path.join(temp_dir, "ml-1m.zip")
    subprocess.run(['curl', '-L', '-o', zip_path, base_url], check=True)
    
    # Extraire le zip dans ce dossier
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Retourner le chemin du dossier extrait
    return os.path.join(temp_dir, "ml-1m")

def upload_to_hdfs(**context):
    """Upload les fichiers vers HDFS"""
    # Configuration WebHDFS
    webhdfs_url = "http://172.20.0.3:9870/webhdfs/v1"
    user = "airflow"
    
    # Créer le dossier dans HDFS
    hdfs_path = "/user/airflow/movielens"
    mkdir_url = f"{webhdfs_url}{hdfs_path}?op=MKDIRS&user.name={user}"
    response = requests.put(mkdir_url)
    response.raise_for_status()
    
    # Chemin local des fichiers extraits
    local_dir = context['task_instance'].xcom_pull(task_ids='download_movielens_data')
    
    # Upload chaque fichier
    for filename in ['movies.dat', 'ratings.dat', 'users.dat']:
        local_path = os.path.join(local_dir, filename)
        hdfs_file_path = f"{hdfs_path}/{filename}"
        
        # Créer le fichier dans HDFS
        create_url = f"{webhdfs_url}{hdfs_file_path}?op=CREATE&user.name={user}&overwrite=true"
        response = requests.put(create_url, allow_redirects=False)
        response.raise_for_status()
        
        # Upload le contenu du fichier
        upload_url = response.headers['Location']
        with open(local_path, 'rb') as f:
            response = requests.put(upload_url, data=f)
            response.raise_for_status()

def create_hive_tables():
    """Crée les tables Hive pour les données MovieLens"""
    # Utiliser beeline pour exécuter les commandes Hive
    beeline_cmd = """
    beeline -u jdbc:hive2://hive-server:10000 -n airflow -e "
    CREATE DATABASE IF NOT EXISTS movielens;
    USE movielens;
    
    CREATE EXTERNAL TABLE IF NOT EXISTS movies (
        movie_id INT,
        title STRING,
        genres STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '::'
    STORED AS TEXTFILE
    LOCATION '/user/airflow/movielens/movies.dat';
    
    CREATE EXTERNAL TABLE IF NOT EXISTS ratings (
        user_id INT,
        movie_id INT,
        rating INT,
        timestamp BIGINT
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '::'
    STORED AS TEXTFILE
    LOCATION '/user/airflow/movielens/ratings.dat';
    
    CREATE EXTERNAL TABLE IF NOT EXISTS users (
        user_id INT,
        gender STRING,
        age INT,
        occupation INT,
        zip_code STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '::'
    STORED AS TEXTFILE
    LOCATION '/user/airflow/movielens/users.dat';
    "
    """
    subprocess.run(beeline_cmd, shell=True, check=True)

with DAG(
    'movielens_ingestion',
    default_args=default_args,
    description='Ingestion des données MovieLens dans HDFS et Hive',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['movielens', 'ingestion'],
) as dag:

    download_task = PythonOperator(
        task_id='download_movielens_data',
        python_callable=download_movielens_data,
    )

    upload_task = PythonOperator(
        task_id='upload_to_hdfs',
        python_callable=upload_to_hdfs,
    )

    create_tables_task = PythonOperator(
        task_id='create_hive_tables',
        python_callable=create_hive_tables,
    )

    download_task >> upload_task >> create_tables_task 