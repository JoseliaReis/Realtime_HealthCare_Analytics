import os
import time
import random
import json
import asyncio
from asyncio import log

from aiokafka.consumer import AIOKafkaConsumer

from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from aiocassandra import aiosession
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

#Configuration
topic =  os.environ.get('SENSOR_TOPIC')
kafka_broker_url = os.environ.get('KAFKA_BROKER_URL')

print("Connecting to Cassandra DB")
cluster = Cluster(
    contact_points=['127.0.0.1'],
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
)
session = cluster.connect()
session.set_keyspace("healthcare_db")


async def consume_payload(loop):
    """
    function to consume from topic and persist to database
    """

    aiosession(session) # create cassandra.cluster.aiosession

    # non-blocking prepared CQL statement
    query = await session.prepare_future('INSERT INTO healthcare_db.device_patient JSON VALUES (?);')
    select = await session.prepare_future('SELECT COUNT(*) healthcare_db.device_patient;')


    # create consumer object
    consumer = AIOKafkaConsumer(
        topic,
        loop=loop,
        bootstrap_servers=kafka_broker_url,
        group_id = "sensor_consumer_group", #Removed as issue with consumer group id
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )
    await consumer.start()

    batch = []

    try:
        async for message in consumer:
            payload = message.value
            deserialized = lambda value: json.loads(payload)
            batch.append(payload)
            statement = SimpleStatement(query, consistency_level=ConsistencyLevel.QUORUM)
            if len(batch) == 100:
                await consumer.commit() #Removed as issue with consumer group id
                batch = []
                persist = session.execute_async(statement,batch)
                persist.add_callbacks(handle_success, handle_error)
                async with session.execute_async(statement,batch) as paginator:
                    async for row in paginator:
                        persist = session.execute_async(row)
                        persist.add_callbacks(handle_success, handle_error)

        session.execute_async(SimpleStatement(select))
    finally:
        await consumer.stop()


def handle_success(rows):
    """function to handle successful callback
    """
    payload = rows[0]
    try:
        consume_payload(payload.id, payload.type, payload.content)
    except Exception:
        log.error("Failed to process payload %s", payload.id)
        # don't re-raise errors in the callback

def handle_error(exception):
    """function to handle unsuccessful callback
    """
    log.error("Failed to fetch payload info: %s", exception)


if __name__ == '__main__':
   # Setup to properly handle KeyboardInterrupt exception
    loop = asyncio.get_event_loop()
    m_task = loop.create_task(consume_payload(loop))
    m_task.add_done_callback(lambda task, loop=loop: loop.stop())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        m_task.cancel()
        loop.run_forever()
    finally:
        if not m_task.cancelled():
            m_task.result()
