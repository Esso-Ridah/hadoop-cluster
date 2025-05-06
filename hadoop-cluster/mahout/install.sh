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
