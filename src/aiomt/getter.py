import aiohttp
import asyncio
import logging
import aiohttp.web as aioweb
from typing import AnyStr, Union, Dict, List
from config import Config

class RequestsFactory:
    @staticmethod
    async def get_json(url):
        return await RequestsFactory.get(url, is_json=True)

    @staticmethod
    async def get_text(url):
        return await RequestsFactory.get(url)

    @staticmethod
    async def get(url: AnyStr, is_json=False) -> Union[Dict, AnyStr]:

        await Config.internal.semaphore_batch.acquire()
        if not Config.internal.parallel:
            await Config.internal.lock.acquire()

        await asyncio.sleep(Config.internal.pick_rand_delay)

        async with aiohttp.ClientSession() as session:

            retries = Config.internal.max_retries

            while retries > 0:
                async with session.get(url, proxy=Config.internal.proxy) as resp:
                    try:
                        if not is_json:
                            result = await resp.text()
                        else:
                            result = await resp.json()

                    except aioweb.HTTPError as e:
                        logging.error(url + ' ' + repr(e))
                        retries -= 1
                        if retries:  # if > 0
                            await asyncio.sleep(Config.internal.retry_delay)
                        else:
                            result = e
                    else:
                        break

            Config.internal.semaphore_batch.release()
            if not Config.internal.parallel:
                Config.internal.lock.release()

            await asyncio.sleep(0)  # next code is computational, let other requests finish

            if isinstance(result, Exception):  # ensure that everything is released, then raise
                raise result

            return result
