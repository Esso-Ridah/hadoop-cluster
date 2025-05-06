# Configuration Airflow pour Hadoop

Ce projet propose deux configurations d'Airflow pour travailler avec Hadoop :

## 1. Configuration de Développement (TP)

La configuration de développement est optimisée pour les TP et l'apprentissage :
- Installation minimale
- Pas de sécurité Kerberos
- Configuration simple et rapide

Pour utiliser cette configuration :
```bash
docker-compose -f docker-compose.dev.yml up -d
```

## 2. Configuration Production (Sécurisée)

La configuration production inclut la sécurité Kerberos, similaire à un environnement professionnel :
- Authentification Kerberos
- Sécurité renforcée
- Configuration plus complexe

Pour utiliser cette configuration :
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Structure des Fichiers

- `Dockerfile.dev` : Configuration de développement
- `Dockerfile.prod` : Configuration production avec Kerberos
- `docker-compose.dev.yml` : Compose pour le développement
- `docker-compose.prod.yml` : Compose pour la production
- `kerberos/` : Dossier contenant les fichiers de configuration Kerberos

## Apprentissage Progressif

1. **Niveau 1 - Bases** (Configuration dev)
   - Comprendre Airflow
   - Créer des DAGs simples
   - Interagir avec Hadoop

2. **Niveau 2 - Sécurité** (Configuration prod)
   - Comprendre Kerberos
   - Gérer l'authentification
   - Sécuriser les workflows

## Ressources Additionnelles

- [Documentation Kerberos](https://web.mit.edu/kerberos/)
- [Sécurité Hadoop](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/SecureMode.html)
- [Airflow Security](https://airflow.apache.org/docs/apache-airflow/stable/security/index.html) 