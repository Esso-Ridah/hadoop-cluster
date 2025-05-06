from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hdfs.hooks.hdfs import HDFSHook
import random

# Arguments par défaut pour le DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Fonction qui simule une opération de traitement de données
def process_data(**kwargs):
    # Simulation d'un traitement qui peut échouer aléatoirement
    if random.random() < 0.3:  # 30% de chance d'échec
        raise Exception("Erreur simulée dans le traitement des données!")
    
    print("✅ Traitement des données réussi!")
    return "Données traitées avec succès"

# Fonction qui simule une opération de validation
def validate_results(**kwargs):
    # Récupération du résultat de la tâche précédente
    ti = kwargs['ti']
    previous_result = ti.xcom_pull(task_ids='process_data')
    print(f"Résultat reçu: {previous_result}")
    
    # Simulation d'une validation
    if random.random() < 0.2:  # 20% de chance d'échec
        raise Exception("Erreur de validation!")
    
    print("✅ Validation réussie!")
    return "Validation terminée"

# Création du DAG
with DAG(
    'example_hadoop_workflow',
    default_args=default_args,
    description='Un DAG d\'exemple pour illustrer les concepts d\'Airflow',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['example', 'hadoop'],
) as dag:

    # Tâche 1: Vérification de l'espace HDFS
    check_hdfs = BashOperator(
        task_id='check_hdfs_space',
        bash_command='echo "Vérification de l\'espace HDFS..." && sleep 2 && echo "Espace disponible: 500GB"',
    )

    # Tâche 2: Traitement des données
    process_task = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
        provide_context=True,
    )

    # Tâche 3: Validation des résultats
    validate_task = PythonOperator(
        task_id='validate_results',
        python_callable=validate_results,
        provide_context=True,
    )

    # Tâche 4: Nettoyage
    cleanup = BashOperator(
        task_id='cleanup',
        bash_command='echo "Nettoyage des fichiers temporaires..." && sleep 1 && echo "Nettoyage terminé"',
    )

    # Définition des dépendances
    check_hdfs >> process_task >> validate_task >> cleanup 
