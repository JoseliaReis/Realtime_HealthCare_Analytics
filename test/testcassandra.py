"FROM https://github.com/aio-libs/aiocassandra/blob/master/example.py"

import asyncio

import pandas as pd
from aiocassandra import aiosession
from cassandra.cluster import Cluster




async def read_cassandra():
    """
    https://github.com/aio-libs/aiocassandra/blob/master/example.py

    :return:
    """
    # patches and adds `execute_future`, `execute_futures` and `prepare_future`
    # to `cassandra.cluster.Session`
    aiosession(session)

    # if non-blocking prepared statements is really needed:
    query = await session.prepare_future('SELECT * FROM healthcare_db.device_patient')

    df = pd.DataFrame(await session.execute_future(query))


loop = asyncio.get_event_loop()
loop.run_until_complete(read_cassandra())

