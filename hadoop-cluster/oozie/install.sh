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
