from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def test_hive_connection():
    """Test la connexion à Hive via beeline"""
    # Test 1: Vérifier la connexion et lister les bases de données
    list_dbs_cmd = """
    beeline -u jdbc:hive2://hive-server:10000 -n airflow -e "SHOW DATABASES;"
    """
    result = subprocess.run(list_dbs_cmd, shell=True, capture_output=True, text=True)
    print("Bases de données disponibles:")
    print(result.stdout)
    
    # Test 2: Créer une base de données de test
    create_db_cmd = """
    beeline -u jdbc:hive2://hive-server:10000 -n airflow -e "
    CREATE DATABASE IF NOT EXISTS test_connection;
    USE test_connection;
    "
    """
    result = subprocess.run(create_db_cmd, shell=True, capture_output=True, text=True)
    print("\nCréation de la base de données de test:")
    print(result.stdout)
    
    # Test 3: Créer une table de test
    create_table_cmd = """
    beeline -u jdbc:hive2://hive-server:10000 -n airflow -e "
    USE test_connection;
    CREATE TABLE IF NOT EXISTS test_table (
        id INT,
        name STRING
    );
    "
    """
    result = subprocess.run(create_table_cmd, shell=True, capture_output=True, text=True)
    print("\nCréation de la table de test:")
    print(result.stdout)
    
    # Test 4: Vérifier que la table existe
    show_tables_cmd = """
    beeline -u jdbc:hive2://hive-server:10000 -n airflow -e "
    USE test_connection;
    SHOW TABLES;
    "
    """
    result = subprocess.run(show_tables_cmd, shell=True, capture_output=True, text=True)
    print("\nTables dans la base de données de test:")
    print(result.stdout)
    
    return "Tests Hive réussis!"

with DAG(
    'test_hive_connection',
    default_args=default_args,
    description='Test de la connexion à Hive',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['test', 'hive'],
) as dag:

    test_task = PythonOperator(
        task_id='test_hive_connection',
        python_callable=test_hive_connection,
    ) 