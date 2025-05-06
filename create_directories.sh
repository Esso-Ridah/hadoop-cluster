#!/bin/bash

# Create Hadoop directories
mkdir -p hadoop/namenode
mkdir -p hadoop/datanode1
mkdir -p hadoop/datanode2
mkdir -p hadoop/datanode3

# Create Hive directories
mkdir -p hive/metastore
mkdir -p hive/warehouse

# Create Pig directory
mkdir -p pig/scripts

# Create Mahout directories
mkdir -p mahout/scripts
mkdir -p mahout/data

# Create ZooKeeper directories
mkdir -p zookeeper/data
mkdir -p zookeeper/datalog

# Create Oozie directories
mkdir -p oozie/data
mkdir -p oozie/conf
mkdir -p oozie/logs
mkdir -p oozie/workflows

# Set permissions
chmod -R 777 hadoop
chmod -R 777 hive
chmod -R 777 pig
chmod -R 777 mahout
chmod -R 777 zookeeper
chmod -R 777 oozie

echo "All directories created successfully!" 