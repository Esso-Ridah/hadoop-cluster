from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def test_hdfs_connection():
    """Test la connexion à HDFS via WebHDFS"""
    # Configuration WebHDFS
    webhdfs_url = "http://172.20.0.3:9870/webhdfs/v1"
    user = "airflow"
    
    # Test 1: Lister le contenu du répertoire racine
    list_url = f"{webhdfs_url}/?op=LISTSTATUS&user.name={user}"
    response = requests.get(list_url)
    response.raise_for_status()
    print("Contenu du répertoire racine HDFS:")
    print(response.json())
    
    # Test 2: Créer un répertoire de test
    test_dir = "/user/airflow/test_connection"
    mkdir_url = f"{webhdfs_url}{test_dir}?op=MKDIRS&user.name={user}"
    response = requests.put(mkdir_url)
    response.raise_for_status()
    print(f"\nRépertoire de test créé: {test_dir}")
    
    # Test 3: Vérifier que le répertoire existe
    list_test_url = f"{webhdfs_url}{test_dir}?op=LISTSTATUS&user.name={user}"
    response = requests.get(list_test_url)
    response.raise_for_status()
    print(f"\nContenu du répertoire de test:")
    print(response.json())
    
    return "Tests HDFS réussis!"

with DAG(
    'test_hdfs_connection',
    default_args=default_args,
    description='Test de la connexion à HDFS',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['test', 'hdfs'],
) as dag:

    test_task = PythonOperator(
        task_id='test_hdfs_connection',
        python_callable=test_hdfs_connection,
    ) 