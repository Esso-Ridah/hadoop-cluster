#!/bin/bash

# Configuration
OOZIE_VERSION="5.2.1"
OOZIE_URL="https://archive.apache.org/dist/oozie/${OOZIE_VERSION}/oozie-${OOZIE_VERSION}.tar.gz"
OOZIE_HOME="/usr/lib/oozie"
OOZIE_DATA="/var/lib/oozie"
OOZIE_LOG="/var/log/oozie"
OOZIE_PID="/var/run/oozie"
OOZIE_TMP="/tmp/oozie"

# Configuration des sources APT pour Debian Bullseye
echo "Configuration des sources APT..."
cat > /etc/apt/sources.list << EOF
deb http://deb.debian.org/debian bullseye main contrib non-free
deb http://security.debian.org/debian-security bullseye-security main contrib non-free
deb http://deb.debian.org/debian bullseye-updates main contrib non-free
EOF

# Mise à jour des sources APT et installation des dépendances
echo "Mise à jour des sources APT et installation des dépendances..."
apt-get clean
apt-get update && \
apt-get install -y --no-install-recommends \
    wget \
    tar \
    gzip \
    openjdk-8-jdk \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Création des répertoires nécessaires
echo "Création des répertoires..."
mkdir -p ${OOZIE_HOME} ${OOZIE_DATA} ${OOZIE_LOG} ${OOZIE_PID} ${OOZIE_TMP}

# Téléchargement d'Oozie
echo "Téléchargement d'Oozie depuis ${OOZIE_URL}..."
if ! wget -q "${OOZIE_URL}" -O /tmp/oozie.tar.gz; then
    echo "Erreur lors du téléchargement d'Oozie"
    exit 1
fi

# Vérification de l'archive
echo "Vérification de l'archive..."
if ! tar -tzf /tmp/oozie.tar.gz > /dev/null 2>&1; then
    echo "L'archive téléchargée est corrompue"
    exit 1
fi

# Extraction de l'archive
echo "Extraction de l'archive..."
if ! tar -xzf /tmp/oozie.tar.gz -C /tmp; then
    echo "Erreur lors de l'extraction de l'archive"
    exit 1
fi

# Vérification de la structure extraite
echo "Vérification de la structure extraite..."
if [ ! -d "/tmp/oozie-${OOZIE_VERSION}" ]; then
    echo "La structure de l'archive n'est pas celle attendue"
    exit 1
fi

# Copie des fichiers
echo "Copie des fichiers..."
cp -r "/tmp/oozie-${OOZIE_VERSION}"/* ${OOZIE_HOME}/

# Nettoyage
echo "Nettoyage..."
rm -rf /tmp/oozie.tar.gz "/tmp/oozie-${OOZIE_VERSION}"

# Vérification de l'installation
echo "Vérification de l'installation..."
if [ ! -f "${OOZIE_HOME}/bin/oozie-setup.sh" ]; then
    echo "Le fichier oozie-setup.sh n'a pas été trouvé après l'installation"
    exit 1
fi

# Configuration d'Oozie
echo "Configuration d'Oozie..."
cat > ${OOZIE_HOME}/conf/oozie-site.xml << EOF
<?xml version="1.0"?>
<configuration>
    <property>
        <name>oozie.service.JPAService.jdbc.driver</name>
        <value>org.postgresql.Driver</value>
    </property>
    <property>
        <name>oozie.service.JPAService.jdbc.url</name>
        <value>jdbc:postgresql://hive-metastore:5432/metastore</value>
    </property>
    <property>
        <name>oozie.service.JPAService.jdbc.username</name>
        <value>hive</value>
    </property>
    <property>
        <name>oozie.service.JPAService.jdbc.password</name>
        <value>hive</value>
    </property>
    <property>
        <name>oozie.service.HadoopAccessorService.hadoop.configurations</name>
        <value>*=/opt/hadoop/etc/hadoop</value>
    </property>
    <property>
        <name>oozie.service.WorkflowAppService.system.libpath</name>
        <value>/user/oozie/share/lib</value>
    </property>
    <property>
        <name>oozie.service.ELService.ext.functions.workflow</name>
        <value>org.apache.oozie.extensions.org.apache.oozie.extensions.hadoop.HadoopELFunction</value>
    </property>
</configuration>
EOF

# Initialisation de la base de données
echo "Initialisation de la base de données..."
${OOZIE_HOME}/bin/oozie-setup.sh db create -run

# Démarrage d'Oozie
echo "Démarrage d'Oozie..."
${OOZIE_HOME}/bin/oozied.sh start

# Vérification du démarrage
echo "Vérification du démarrage..."
sleep 10
if ! curl -s http://localhost:11000/oozie > /dev/null; then
    echo "Oozie n'a pas démarré correctement"
    exit 1
fi

echo "Installation et configuration d'Oozie terminées avec succès"
