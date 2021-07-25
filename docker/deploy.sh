
#!/bin/bash
cd ./docker
# Stop the App
echo "--- Start Healthcare Data Pipline Deployment --- "

# Create network
echo -n " Create Kafka Pipeline Network"
sudo docker network create healthcare_data_pipeline

# Create kafka cluster
echo -n " Create Kafka Cluster with Zookeeper & Broker "
sudo docker-compose -f docker-compose-kafka.yaml up -d


# Create Database

#Cassandra
echo -n " Create Cassandra Database from Bootstrap file "
sudo docker-compose -f docker-compose-cassandra.yaml up -d


# Build all
echo -n "Build Apps"
sudo docker-compose up --build


echo "--- Deployment Complete --- "
