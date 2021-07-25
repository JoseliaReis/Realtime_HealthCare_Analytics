import os
import random
import json
import asyncio
from aiokafka.producer import AIOKafkaProducer
from content_generator import create_patient_content, create_sensor_content

#Configuration
topic =  os.environ.get('SENSOR_TOPIC')
kafka_broker_url = os.environ.get('KAFKA_BROKER_URL')

def serializer(data):
    """
    function to serialize dict to json
    """
    return json.dumps(data).encode()

async def produce_payload(sensor_count, patient_count, loop):
    """
    function to transform payload and batch append to kafka producer
    """
    producer = AIOKafkaProducer(
        bootstrap_servers=kafka_broker_url,
        loop=loop,
    )
    await producer.start()

    batch = producer.create_batch()

    for i in range(patient_count):
        print("Generating Patient Data for {0} patients".format(patient_count))
        patient: dict = create_patient_content()
        for j in range(sensor_count):
            # create the payload/sensor content
            sensor: dict = create_sensor_content()
            # join the patient data
            # ** to join two different dictionary
            records: dict = {**patient, **sensor}
            serialized = serializer(records)
            metadata = batch.append(key=None, value=serialized, timestamp=None)
            if metadata is None:
                partitions = await producer.partitions_for(topic)
                partition = random.choice(tuple(partitions))
                await producer.send_batch(batch, topic, partition=partition)
                print("%d messages sent to partition %d"
                      % (batch.record_count(), partition))
                batch = producer.create_batch()

    partitions = await producer.partitions_for(topic)
    partition = random.choice(tuple(partitions))
    await producer.send_batch(batch, topic, partition=partition)
    print("%d messages sent to partition %d"
          % (batch.record_count(), partition))
    await producer.stop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(produce_payload(50,10000, loop))
    loop.close()


