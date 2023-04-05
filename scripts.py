import asyncio

from sql import init_models


def recreate_tables():
    asyncio.run(init_models())