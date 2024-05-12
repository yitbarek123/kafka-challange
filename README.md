# Kafka challange
This project simulates producing data and consuming it in a publish-subscribe manner using Kafka. The producer generates a stream of data with a specific topic, and a consumer can access the data if subscribed to that topic. The main requirement of this challenge is to count the unique IDs for each minute. The solution appends IDs to a list until the timestamp difference exceeds 1 minute, then counts the unique elements of the list.

## Table of Contents

- [Build](#Build)
- [Run](#Run)
- [Features](#Features)
- [Sugestions](#Sugestions)


## Build

Build both the kafka and consumer by using docker-compose. And, download the test data zip file in the same terminal. 

```bash
# clone the repository
git clone git@github.com:yitbarek123/kafka-challange.git
cd kafka-challange
# Download the test data
wget https://tda-public.s3.eu-central-1.amazonaws.com/hire-challenge/stream.jsonl.gz

#build kafka
docker-compose build

#build consumer
docker build -t consumer .
```
## Run

First run the kafka then produce the test data inside kafka container. The test data file exist in the container because it mapped.
```bash
# Run kafka
docker-compose up kafka

# New terminal
# Produce the test data
docker exec -it kafka-challange_kafka_1 bash
zcat gz/stream.jsonl.gz | kafka-console-producer.sh --broker-list localhost:9092 --topic mytopic

# New terminal

# Consume the test data
docker run --network kafka-challange_kafka-netw -it consumer
```

## Features
The execution of the consumer container count minutes, starting from the first time-stamp and prints number of unique Ids for each minute.

## TODO
To achieve better performance, additional workers can be added in pipeline mode to parallelize the overall workload. Furthermore, replacing JSON with Protocol Buffers (protobuf) and using gRPC can improve performance by up to 10 times.