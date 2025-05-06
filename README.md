# Analyse Météorologique avec Hadoop et Airflow

Ce projet permet d'analyser des données météorologiques en utilisant Hadoop pour le traitement distribué et Airflow pour l'orchestration des tâches. Il inclut des DAGs pour l'extraction, la transformation et le chargement des données météorologiques.

## Architecture

Le projet utilise les composants suivants :
- **Hadoop** : Pour le stockage distribué (HDFS) et le traitement des données
- **Hive** : Pour l'analyse des données avec SQL
- **Airflow** : Pour l'orchestration des tâches ETL
- **PostgreSQL** : Pour la base de données Airflow

## Prérequis

- Docker et Docker Compose
- Au moins 8GB de RAM disponible
- Au moins 20GB d'espace disque disponible
- Ports disponibles : 8080 (Airflow), 9870 (HDFS), 10000 (Hive)

## Installation

1. Cloner le dépôt :
```bash
git clone [URL_DU_REPO]
cd hadoop_weather_analysis
```

2. Démarrer l'environnement :
```bash
# Démarrer les services Hadoop et Hive
sudo docker-compose -f hadoop-cluster/docker-compose.yml up -d

# Démarrer les services Airflow
sudo docker-compose -f hadoop-cluster/docker-compose.dev.yml up -d
```

## Structure du Projet

```
hadoop-cluster/
├── airflow/
│   ├── dags/              # DAGs Airflow
│   │   ├── example_etl_dag.py
│   │   ├── test_hdfs_connection.py
│   │   └── test_hive_connection.py
│   ├── logs/             # Logs Airflow
│   └── plugins/          # Plugins Airflow
├── hadoop/
│   ├── namenode/        # Données HDFS namenode
│   └── datanode*/       # Données HDFS datanodes
├── hive/
│   ├── metastore/       # Métadonnées Hive
│   └── warehouse/       # Données Hive
├── docker-compose.yml           # Configuration Hadoop et Hive
└── docker-compose.dev.yml       # Configuration Airflow
```

## DAGs Disponibles

1. **example_etl_dag.py**
   - Tâche 1 : Extraction de données météo et stockage dans HDFS
   - Tâche 2 : Transformation des données et création d'une table Hive
   - Tâche 3 : Création d'une vue agrégée des données

2. **test_hdfs_connection.py**
   - Test de la connexion à HDFS
   - Création d'un répertoire test
   - Vérification des permissions

3. **test_hive_connection.py**
   - Test de la connexion à Hive
   - Création d'une base de données test
   - Création d'une table test

## Utilisation

1. **Accéder à l'interface Airflow**
   - URL : http://localhost:8080
   - Identifiants : airflow/airflow

2. **Vérifier les services**
   - HDFS Web UI : http://localhost:9870
   - Hive Server : localhost:10000

3. **Commandes utiles**
   ```bash
   # Voir les logs des services
   sudo docker logs airflow-web
   sudo docker logs airflow-scheduler
   sudo docker logs namenode
   sudo docker logs hive-server

   # Arrêter les services
   sudo docker-compose -f hadoop-cluster/docker-compose.yml down
   sudo docker-compose -f hadoop-cluster/docker-compose.dev.yml down
   ```

## Dépannage

1. **Problèmes de connexion**
   - Vérifier que tous les services sont en cours d'exécution
   - Vérifier les logs des services
   - S'assurer que les ports ne sont pas déjà utilisés

2. **Problèmes avec les DAGs**
   - Vérifier les logs Airflow
   - S'assurer que les connexions sont correctement configurées
   - Vérifier les permissions HDFS

## Nettoyage

Pour arrêter et nettoyer l'environnement :
```bash
# Arrêter les services
sudo docker-compose -f hadoop-cluster/docker-compose.yml down
sudo docker-compose -f hadoop-cluster/docker-compose.dev.yml down

# Supprimer les volumes (optionnel)
sudo docker-compose -f hadoop-cluster/docker-compose.yml down -v
sudo docker-compose -f hadoop-cluster/docker-compose.dev.yml down -v
```

## Ressources

- [Documentation Airflow](https://airflow.apache.org/docs/)
- [Documentation Hadoop](https://hadoop.apache.org/docs/current/)
- [Documentation Hive](https://cwiki.apache.org/confluence/display/Hive/Home)

# Installation du Cluster Hadoop avec Pig, Mahout et Oozie

Ce guide explique comment installer et configurer un cluster Hadoop avec les services Pig, Mahout et Oozie.

## Prérequis

- Docker
- Docker Compose
- Au moins 8GB de RAM disponible
- Au moins 20GB d'espace disque disponible

## Installation

1. Clonez le dépôt :
```bash
git clone <url-du-repo>
cd hadoop-cluster
```

2. Rendez le script d'installation exécutable :
```bash
chmod +x setup.sh
```

3. Exécutez le script d'installation :
```bash
./setup.sh
```

Ce script va :
- Créer les répertoires nécessaires pour Pig, Mahout et Oozie
- Générer les scripts d'installation pour chaque service
- Créer des exemples de fichiers de configuration
- Rendre tous les scripts exécutables

## Démarrage des Services

1. Démarrez tous les services avec Docker Compose :
```bash
docker-compose up -d
```

2. Vérifiez que tous les services sont en cours d'exécution :
```bash
docker-compose ps
```

3. Pour voir les logs des services :
```bash
docker-compose logs -f pig-server mahout-server oozie
```

## Structure des Répertoires

```
hadoop-cluster/
├── pig/
│   ├── install.sh
│   └── scripts/
│       └── example.pig
├── mahout/
│   ├── install.sh
│   ├── scripts/
│   │   └── example.sh
│   └── data/
├── oozie/
│   ├── install.sh
│   ├── data/
│   ├── conf/
│   ├── logs/
│   └── workflows/
│       └── workflow.xml
└── docker-compose.yml
```

## Configuration des Services

### Pig
- Le script d'installation est dans `pig/install.sh`
- Les scripts Pig sont stockés dans `pig/scripts/`
- Un exemple de script est fourni dans `pig/scripts/example.pig`

### Mahout
- Le script d'installation est dans `mahout/install.sh`
- Les scripts Mahout sont stockés dans `mahout/scripts/`
- Les données sont stockées dans `mahout/data/`
- Un exemple de script est fourni dans `mahout/scripts/example.sh`

### Oozie
- Le script d'installation est dans `oozie/install.sh`
- Les workflows sont stockés dans `oozie/workflows/`
- Les logs sont dans `oozie/logs/`
- La configuration est dans `oozie/conf/`
- Un exemple de workflow est fourni dans `oozie/workflows/workflow.xml`

## Dépannage

Si vous rencontrez des problèmes :

1. Vérifiez les logs des services :
```bash
docker-compose logs -f <nom-du-service>
```

2. Redémarrez un service spécifique :
```bash
docker-compose restart <nom-du-service>
```

3. Reconstruire un service :
```bash
docker-compose up -d --build <nom-du-service>
```

## Arrêt des Services

Pour arrêter tous les services :
```bash
docker-compose down
```

Pour arrêter et supprimer les volumes :
```bash
docker-compose down -v
```

## Notes Importantes

- Assurez-vous que HDFS est prêt avant d'utiliser Pig, Mahout ou Oozie
- Les services peuvent prendre plusieurs minutes pour démarrer complètement
- Consultez les logs si un service ne démarre pas correctement
- Les données persistantes sont stockées dans les volumes Docker

# Guide d'Installation - Environnement Hadoop avec Airflow

## Prérequis

1. **Système d'exploitation**
   - Linux (Ubuntu 20.04 ou supérieur recommandé)
   - Au moins 8GB de RAM
   - Au moins 20GB d'espace disque libre

2. **Installation des dépendances**
   ```bash
   # Mise à jour du système
   sudo apt update && sudo apt upgrade -y

   # Installation de Docker et Docker Compose
   sudo apt install -y docker.io docker-compose
   sudo systemctl enable docker
   sudo systemctl start docker
   sudo usermod -aG docker $USER
   ```

3. **Redémarrage de session**
   - Déconnectez-vous et reconnectez-vous pour que les changements de groupe prennent effet

## Structure du Projet

1. **Création du répertoire de travail**
   ```bash
   mkdir -p ~/hadoop_weather_analysis
   cd ~/hadoop_weather_analysis
   ```

2. **Cloner le dépôt (à adapter selon votre méthode de distribution)**
   ```bash
   # Si vous utilisez Git
   git clone <votre-repo> hadoop-cluster
   cd hadoop-cluster
   ```

## Configuration d'Airflow

1. **Structure des fichiers Airflow**
   ```
   hadoop-cluster/
   └── airflow/
       ├── config/
       │   └── connections.json
       ├── dags/
       │   └── test_connections.py
       ├── scripts/
       │   └── import_connections.py
       └── Dockerfile
   ```

2. **Configuration des connexions**
   Créez le fichier `airflow/config/connections.json` :
   ```json
   [
     {
       "conn_id": "hdfs_default",
       "conn_type": "hdfs",
       "host": "namenode",
       "port": 8020,
       "login": "airflow",
       "extra": {
         "use_kerberos": false
       }
     },
     {
       "conn_id": "webhdfs_default",
       "conn_type": "webhdfs",
       "host": "namenode",
       "port": 9870,
       "login": "airflow",
       "extra": {
         "use_kerberos": false
       }
     },
     {
       "conn_id": "hive_default",
       "conn_type": "hive",
       "host": "hive-server",
       "port": 10000,
       "login": "airflow",
       "schema": "default"
     },
     {
       "conn_id": "spark_default",
       "conn_type": "spark",
       "host": "spark-master",
       "port": 7077,
       "extra": {
         "queue": "default"
       }
     }
   ]
   ```

3. **DAG de test**
   Créez le fichier `airflow/dags/test_connections.py` :
   ```python
   from airflow import DAG
   from airflow.providers.apache.hdfs.hooks.hdfs import HDFSHook
   from airflow.operators.python import PythonOperator
   from datetime import datetime, timedelta

   def check_hdfs_conn(**kwargs):
       hook = HDFSHook('hdfs_default')
       client = hook.get_conn()
       client.listStatus('/')  # lève si KO

   default_args = {
       'owner': 'airflow',
       'retries': 1,
       'retry_delay': timedelta(minutes=5),
       'start_date': datetime(2025,1,1),
   }

   with DAG('test_hdfs_connection',
            default_args=default_args,
            schedule_interval=None,
            catchup=False) as dag:

       t1 = PythonOperator(
           task_id='check_hdfs',
           python_callable=check_hdfs_conn,
           provide_context=True,
       )
   ```

4. **Script d'import des connexions**
   Créez le fichier `airflow/scripts/import_connections.py` :
   ```python
   #!/usr/bin/env python3
   import json
   import os
   from airflow import settings
   from airflow.models import Connection
   from sqlalchemy.orm import Session

   def import_connections():
       config_dir = os.getenv('AIRFLOW_HOME', '/opt/airflow') + '/config'
       path = os.path.join(config_dir, 'connections.json')
       if not os.path.isfile(path):
           print(f"⚠️  Fichier non trouvé : {path}")
           return

       with open(path) as f:
           data = json.load(f)

       if isinstance(data, dict):
           connections = list(data.values())
       elif isinstance(data, list):
           connections = data
       else:
           raise ValueError("Le fichier connections.json doit être un list ou un dict racine")

       session: Session = settings.Session()
       for conn in connections:
           cid = conn.get('conn_id')
           if not cid:
               continue
           existing = session.query(Connection).filter_by(conn_id=cid).first()
           if existing:
               print(f"🔄 Update {cid}")
               for attr in ('conn_type','host','login','password','schema','port'):
                   if conn.get(attr) is not None:
                       setattr(existing, attr, conn[attr])
               if conn.get('extra') is not None:
                   existing.set_extra(conn['extra'])
           else:
               print(f"➕ Create {cid}")
               new = Connection(
                   conn_id=cid,
                   conn_type=conn.get('conn_type'),
                   host=conn.get('host'),
                   login=conn.get('login'),
                   password=conn.get('password'),
                   schema=conn.get('schema'),
                   port=conn.get('port'),
               )
               if conn.get('extra'):
                   new.set_extra(conn['extra'])
               session.add(new)
       session.commit()
       session.close()
       print("✅ Import terminé")

   if __name__ == "__main__":
       import_connections()
   ```

## Démarrage des Services

1. **Lancement d'Airflow**
   ```bash
   # Arrêt des services existants
   docker-compose -f docker-compose.dev.yml down

   # Construction de l'image
   docker-compose -f docker-compose.dev.yml build --no-cache airflow-web

   # Démarrage du service
   docker-compose -f docker-compose.dev.yml up -d airflow-web

   # Vérification des logs
   docker-compose -f docker-compose.dev.yml logs -f airflow-web
   ```

2. **Vérification**
   - Attendez que les logs indiquent que le service est prêt
   - Vérifiez que vous voyez les messages de mise à jour des connexions
   - Le webserver devrait être accessible sur http://localhost:8080

## Dépannage

1. **Problèmes courants**
   - Si les connexions ne sont pas importées, vérifiez le format du fichier `connections.json`
   - Si le DAG n'apparaît pas, vérifiez les logs pour les erreurs d'importation
   - Si le service ne démarre pas, vérifiez les logs pour les erreurs de configuration

2. **Commandes utiles**
   ```bash
   # Voir les logs en temps réel
   docker-compose -f docker-compose.dev.yml logs -f airflow-web

   # Redémarrer le service
   docker-compose -f docker-compose.dev.yml restart airflow-web

   # Voir les conteneurs en cours d'exécution
   docker-compose -f docker-compose.dev.yml ps
   ```

## Prochaines étapes

Une fois que tout est installé et fonctionnel, nous pourrons :
1. Créer l'utilisateur admin Airflow
2. Lancer les autres services (Hadoop, Hive, etc.)
3. Commencer les TP pratiques 

# TP Hadoop & Airflow - Analyse de Données Météo

Ce projet met en place un environnement de traitement de données avec Hadoop, Hive et Airflow pour l'analyse de données météorologiques.

## Architecture

- **Hadoop** : Stockage distribué (HDFS) et traitement (MapReduce)
- **Hive** : Data warehouse pour requêtes SQL
- **Airflow** : Orchestration des workflows
- **PostgreSQL** : Base de données pour Airflow

## Prérequis

- Docker et Docker Compose
- Git
- Au moins 4GB de RAM disponible
- Ports 8080, 9870, 10000 disponibles

## Installation

1. Cloner le repository :
```bash
git clone [URL_DU_REPO]
cd hadoop_weather_analysis
```

2. Démarrer l'environnement :
```bash
cd hadoop-cluster
docker-compose -f docker-compose.dev.yml up -d
```

3. Attendre que tous les services soient démarrés (environ 2-3 minutes)

4. Accéder aux interfaces :
   - Airflow : http://localhost:8080 (user: airflow, password: airflow)
   - HDFS : http://localhost:9870
   - Hive : via beeline (port 10000)

## Structure du Projet

```
hadoop_weather_analysis/
├── hadoop-cluster/
│   ├── docker-compose.dev.yml    # Configuration Docker
│   ├── airflow/
│   │   └── dags/                 # DAGs Airflow
│   │       ├── example_etl_dag.py    # DAG principal
│   │       ├── test_hdfs_connection.py
│   │       └── test_hive_connection.py
│   └── scripts/                  # Scripts utilitaires
└── README.md
```

## DAGs Disponibles

1. **example_etl_dag.py**
   - Processus ETL complet
   - 3 tâches : extraction, transformation, chargement
   - Utilise HDFS et Hive

2. **test_hdfs_connection.py**
   - Test de connexion à HDFS
   - Création de répertoires et fichiers

3. **test_hive_connection.py**
   - Test de connexion à Hive
   - Création de base de données et tables

## Utilisation

### 1. Vérifier les Services

```bash
docker ps
```
Vérifier que tous les services sont en état "Up" :
- namenode
- datanode
- hive-server
- airflow-web
- airflow-scheduler
- postgres

### 2. Tester les Connexions

créer un user: 
```bash
docker exec -it airflow-web airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin
```
1. Dans l'interface Airflow (http://localhost:8080) :
   - Activer le DAG `test_hdfs_connection`
   - Déclencher une exécution manuelle
   - Vérifier les logs

2. Répéter avec `test_hive_connection`

### 3. Exécuter le DAG Principal

1. Activer `example_etl_dag`
2. Déclencher une exécution
3. Suivre l'exécution dans l'interface
4. Vérifier les résultats dans Hive

## Commandes Utiles

### HDFS
```bash
# Lister les fichiers
docker exec namenode hdfs dfs -ls /user/airflow

# Voir le contenu d'un fichier
docker exec namenode hdfs dfs -cat /user/airflow/weather_data/*
```

### Hive
```bash
# Se connecter à Hive
docker exec -it hive-server beeline -u jdbc:hive2://localhost:10000 -n airflow

# Requêtes utiles
SHOW DATABASES;
USE weather_db;
SHOW TABLES;
SELECT * FROM weather_summary;
```

### Airflow
```bash
# Voir les logs d'un DAG
docker logs airflow-scheduler

# Redémarrer un service
docker-compose -f docker-compose.dev.yml restart airflow-web
```

## Dépannage

1. **Airflow ne démarre pas**
   - Vérifier les logs : `docker logs airflow-web`
   - Redémarrer : `docker-compose -f docker-compose.dev.yml restart airflow-web`

2. **HDFS inaccessible**
   - Vérifier que namenode est en cours d'exécution
   - Vérifier les logs : `docker logs namenode`

3. **Hive ne répond pas**
   - Vérifier que hive-server est en cours d'exécution
   - Vérifier les logs : `docker logs hive-server`

## Nettoyage

Pour arrêter et nettoyer l'environnement :
```bash
docker-compose -f docker-compose.dev.yml down -v
```

## Ressources Additionnelles

- [Documentation Airflow](https://airflow.apache.org/docs/)
- [Documentation Hive](https://cwiki.apache.org/confluence/display/Hive/Home)
- [Documentation HDFS](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html) 
