# Modules Used
* aiokafka - Asynchronous Kafka Streaming
* asyncio - Asynchronous Python Threading
* aiomysl 
* cassandra-driver - Cassandra Connector/Sink
* aiocassandra - Asynchronous Cassandra Writing


#Docker Installation

## Install Docker

## Install Docker-compose
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

$ sudo chmod +x /usr/local/bin/docker-compose

$ docker–compose -–version

# How to Manually RUN

# STEP 1 - CREATE THE DOCKER NETWORK
$ docker network create healthcare_pipeline

#STEP 2 - COMPOSE/BUILD THE KAFKA RESOURCES
 Go to docker folder and run the following command 
$ docker-compose -f docker-compose-kafka.yaml up -d --remove-orphans

#OPTIONAL STEP - CHECK IF KAFKA STARTED
$ docker-compose -f docker-compose-kafka.yaml logs -f broker | grep "started"

# STEP 3 - COMPOSE/BUILD CASSANDRA DATABASE
$ docker-compose -f docker-compose-cassandra.yaml up -d --remove-orphans


# STEP 4 - CONNECT TO CASSANDRA
$ docker exec -it cassandra cqlsh localhost 9042

# STEP 5 - create keyspace

CREATE KEYSPACE IF NOT EXISTS healthcare_db
WITH REPLICATION = {
  'class': 'SimpleStrategy',
  'replication_factor': '3'
};

# STEP 6 -  Use Keyspace
use healthcare_db;

# STEP 7 - Create table

CREATE TABLE IF NOT EXISTS healthcare_db.device_patient(
  id TEXT,
  name TEXT,
  age INT,
  gender TEXT,
  phone TEXT,
  address TEXT,
  condition TEXT,
  bmi DECIMAL,
  status TEXT,
  device_id TEXT, 
  reading_id TEXT,
  heart_rate INT,
  blood_pressure_top INT,
  blood_pressure_bottom INT,
  body_temperature DECIMAL,
  blood_sugar_level INT,
  timestamp TIMESTAMP ,
  longitude TEXT,
  latitude TEXT,
  alert TEXT,
  PRIMARY KEY ((id), timestamp))
WITH CLUSTERING ORDER BY (timestamp DESC);



## STEP 8 - Import Data to Cassandra for testing
go to cassandra folder
run - python import_to_cassandra.py


# STEP 9 - Run the Dashboard
python dashboard.py

### REMOVE EVERYTHING

$ ./destroy.sh


