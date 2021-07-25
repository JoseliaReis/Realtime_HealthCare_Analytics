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


# How to Run

## Deployment/Destroy Clusters + APP

### Deploy Script

$ ./deploy.sh

### Destroy Script

$ ./destory.sh


## MANUAL TEAR DOWN STEPS

### start main docker compose
$ docker network create healthcare_data_pipeline

$ docker-compose -f docker-compose-kafka.yaml up -d

$ docker-compose -f docker-compose-kafka.yaml logs -f broker | grep "started"

$ docker-compose -f docker-compose-mysql.yaml up -d

$ docker-compose up --build


## INTERFACING WITH APP
### View Stream in Topic
$ docker-compose -f docker-compose-kafka.yaml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic queueing.healthcaredata --from-beginning

### View Data via Cassandra Shell

#### Connect to Cassandra Shell
$ docker exec -it cassandra cqlsh localhost 9042 


##### Cassandra shell commands
cqlsh> use sensorpipeline;

cqlsh:sensorpipeline> select * from sensorpipeline.sensordata;

 id | content | type
----+---------+------

(0 rows)

cqlsh:sensorpipeline> exit


## MANUAL TEAR DOWN STEPS

### Stop the App
$ docker-compose down --remove-orphans

### Stop the Kafka cluster
$ docker-compose -f docker-compose-kafka.yaml stop

### Remove Contents of Topics and Kafka cluster
$ docker-compose -f docker-compose-kafka.yaml down

### Stop Cassandra DB
$ docker-compose -f docker-compose-cassandra.yaml down
$ docker rm container cassandra


### Remove Docker network
$ docker network rm sensor_data_pipeline

## Current Outstanding Bugs
* Cassandra Hostname refused connection continues to work intermittently, could not fix without further time spent on debugging.

## Outstanding TODO
* Unittesting
