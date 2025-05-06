 #!/bin/bash

# Création des répertoires nécessaires
echo "Création des répertoires..."
mkdir -p pig/scripts
mkdir -p mahout/scripts
mkdir -p mahout/data
mkdir -p oozie/data
mkdir -p oozie/conf
mkdir -p oozie/logs
mkdir -p oozie/workflows

# Création des scripts d'installation
echo "Création des scripts d'installation..."

# Script d'installation pour Pig
cat > pig/install.sh << 'EOF'
#!/bin/bash

# Update APT sources
echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list
echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list

# Create Hadoop configuration directory
/bin/mkdir -p /opt/hadoop/etc/hadoop

# Copy Hadoop configuration
/bin/cp -r /etc/hadoop/* /opt/hadoop/etc/hadoop/

# Wait for HDFS to be ready
while ! hdfs dfsadmin -report; do
  echo "Waiting for HDFS..."
  sleep 5
done

# Install Pig
apt-get update
apt-get install -y wget tar
wget https://archive.apache.org/dist/pig/pig-0.17.0/pig-0.17.0.tar.gz
tar -xzf pig-0.17.0.tar.gz
mv pig-0.17.0 /opt/pig
ln -s /opt/pig/bin/pig /usr/bin/pig
export PIG_CLASSPATH=/opt/hadoop/etc/hadoop
echo "Pig installation completed"

# Keep container running
while true; do sleep 3600; done
EOF

# Script d'installation pour Mahout
cat > mahout/install.sh << 'EOF'
#!/bin/bash

# Update APT sources
echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list
echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list

# Create Hadoop configuration directory
/bin/mkdir -p /opt/hadoop/etc/hadoop

# Copy Hadoop configuration
/bin/cp -r /etc/hadoop/* /opt/hadoop/etc/hadoop/

# Wait for HDFS to be ready
while ! hdfs dfsadmin -report; do
  echo "Waiting for HDFS..."
  sleep 5
done

# Install Mahout
apt-get update
apt-get install -y wget tar
wget https://archive.apache.org/dist/mahout/0.13.0/apache-mahout-distribution-0.13.0.tar.gz
tar -xzf apache-mahout-distribution-0.13.0.tar.gz
mv apache-mahout-distribution-0.13.0 /opt/mahout
ln -s /opt/mahout/bin/mahout /usr/bin/mahout
echo "Mahout installation completed"

# Keep container running
while true; do sleep 3600; done
EOF

# Script d'installation pour Oozie
cat > oozie/install.sh << 'EOF'
#!/bin/bash

# Update APT sources
echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list
echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list

# Create Hadoop configuration directory
/bin/mkdir -p /opt/hadoop/etc/hadoop

# Copy Hadoop configuration
/bin/cp -r /etc/hadoop/* /opt/hadoop/etc/hadoop/

# Wait for HDFS to be ready
while ! hdfs dfsadmin -report; do
  echo "Waiting for HDFS..."
  sleep 5
done

# Install Oozie
apt-get update
apt-get install -y wget tar openjdk-8-jdk
wget https://archive.apache.org/dist/oozie/5.2.0/oozie-5.2.0.tar.gz
tar -xzf oozie-5.2.0.tar.gz
mv oozie-5.2.0 /usr/lib/oozie
ln -s /usr/lib/oozie/bin/oozie /usr/bin/oozie
/bin/mkdir -p /oozie/data/derby
/usr/lib/oozie/bin/oozie-setup.sh sharelib create -fs hdfs://namenode:9000
/usr/lib/oozie/bin/ooziedb.sh create -sqlfile oozie.sql -run
echo "Oozie installation completed"

# Start Oozie
/usr/lib/oozie/bin/oozied.sh run
EOF

# Rendre les scripts exécutables
echo "Rendre les scripts exécutables..."
chmod +x pig/install.sh
chmod +x mahout/install.sh
chmod +x oozie/install.sh

# Création des fichiers de configuration de base

# Configuration de base pour Pig
cat > pig/scripts/example.pig << 'EOF'
-- Example Pig script
data = LOAD 'input.txt' USING PigStorage(',') AS (field1:chararray, field2:int);
filtered = FILTER data BY field2 > 0;
STORE filtered INTO 'output' USING PigStorage(',');
EOF

# Configuration de base pour Mahout
cat > mahout/scripts/example.sh << 'EOF'
#!/bin/bash
# Example Mahout script
mahout seqdirectory -i /mahout/data/input -o /mahout/data/output
EOF
chmod +x mahout/scripts/example.sh

# Configuration de base pour Oozie
cat > oozie/workflows/workflow.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<workflow-app xmlns="uri:oozie:workflow:0.5" name="example-workflow">
    <start to="first-job"/>
    <action name="first-job">
        <map-reduce>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <configuration>
                <property>
                    <name>mapred.mapper.class</name>
                    <value>org.apache.hadoop.mapred.lib.IdentityMapper</value>
                </property>
                <property>
                    <name>mapred.reducer.class</name>
                    <value>org.apache.hadoop.mapred.lib.IdentityReducer</value>
                </property>
            </configuration>
        </map-reduce>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    <kill name="fail">
        <message>Map/Reduce failed, error message[${wf:errorMessage(wf:lastErrorNode())}]</message>
    </kill>
    <end name="end"/>
</workflow-app>
EOF

echo "Configuration terminée !"
echo "Pour démarrer les services, exécutez :"
echo "docker-compose up -d"
echo "Pour vérifier les logs :"
echo "docker-compose logs -f pig-server mahout-server oozie"
