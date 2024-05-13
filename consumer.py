from confluent_kafka import Consumer, KafkaError,KafkaException
import datetime
import json
import time
# Kafka broker configuration
bootstrap_servers = 'kafka:9092'  # Use service name as hostname

# Kafka consumer configuration
conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'  # Start consuming from the earliest message
}

# Create Kafka Consumer instance
consumer = Consumer(conf)

# Subscribe to the Kafka topic
topic = 'mytopic'
consumer.subscribe([topic])

def is_difference_exceeds_one_minute(timestamp1, timestamp2):
    # Convert timestamps to datetime objects
    dt1 = datetime.datetime.utcfromtimestamp(timestamp1)
    dt2 = datetime.datetime.utcfromtimestamp(timestamp2)

    # Calculate the absolute difference in seconds
    difference_seconds = abs((dt2 - dt1).total_seconds())

    # Check if the difference exceeds 1 minute (60 seconds)
    return difference_seconds > 60
try:
    start_time=0
    minute_cnt=0
    unique_id=[]
    while True:
        # Poll for new messages
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition
                print('%% %s [%d] reached end at offset %d\n' %
                      (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:

            import datetime

        if start_time==0:
            start_time=int(json.loads(msg.value().decode('utf-8'))['ts'])
            minute_cnt+=1
        # Check if the difference exceeds 1 minute
        if is_difference_exceeds_one_minute(start_time, int(json.loads(msg.value().decode('utf-8'))['ts'])):
            unique_id.append(json.loads(msg.value().decode('utf-8'))['uid'])
            print("The difference between the timestamps exceeds 1 minute.")
            minute_cnt+=1
            result={}
            result["minute"]=minute_cnt
            result["unique_ids"]=len(list(dict.fromkeys(unique_id)))
            print(result)
            unique_id=[]
            start_time=int(json.loads(msg.value().decode('utf-8'))['ts'])

        else:
            if json.loads(msg.value().decode('utf-8'))['uid'] not in unique_id: 
                unique_id.append(json.loads(msg.value().decode('utf-8'))['uid'])
        #time.sleep(4)

except KeyboardInterrupt:
    pass

finally:
    # Close the consumer
    consumer.close()
