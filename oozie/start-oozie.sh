#!/bin/bash

# Configuration Hadoop
export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
export HADOOP_HOME=/opt/hadoop
export OOZIE_HOME=/opt/oozie
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$OOZIE_HOME/bin

# Vérification des scripts Oozie
echo "Vérification des scripts Oozie..."
echo "Contenu du répertoire Oozie :"
ls -la ${OOZIE_HOME}
echo "Contenu du répertoire bin :"
ls -la ${OOZIE_HOME}/bin

# Créer la configuration Hadoop
mkdir -p $HADOOP_CONF_DIR
cat > $HADOOP_CONF_DIR/core-site.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://namenode:9000</value>
    </property>
</configuration>
EOF

# Vérifier la configuration
echo "Configuration Hadoop :"
echo "fs.defaultFS: ${CORE_CONF_fs_defaultFS:-hdfs://namenode:9000}"

# Vérifier la résolution DNS
echo "Vérification de la résolution DNS :"
ping -c 1 namenode

# Attendre HDFS
echo "Attente de HDFS disponible..."
until hdfs dfsadmin -report > /dev/null 2>&1; do
    echo "HDFS n'est pas encore prêt, attente..."
    sleep 5
done

echo "HDFS est prêt !"

# Installer Sharelib
echo "Installation de Sharelib..."
if [ -f "${OOZIE_HOME}/bin/oozie-setup.sh" ]; then
    ${OOZIE_HOME}/bin/oozie-setup.sh sharelib create -fs ${CORE_CONF_fs_defaultFS:-hdfs://namenode:9000}
else
    echo "ERREUR: oozie-setup.sh non trouvé dans ${OOZIE_HOME}/bin/"
    exit 1
fi

# Lancer Oozie
echo "Démarrage d'Oozie..."
if [ -f "${OOZIE_HOME}/bin/oozied.sh" ]; then
    ${OOZIE_HOME}/bin/oozied.sh start
else
    echo "ERREUR: oozied.sh non trouvé dans ${OOZIE_HOME}/bin/"
    exit 1
fi

# Garder le conteneur en vie
tail -f ${OOZIE_HOME}/logs/oozie.log 