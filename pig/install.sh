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
