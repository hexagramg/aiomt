from __future__ import annotations
from asyncio import Semaphore, Lock
from random import uniform, choice
from typing import Union, Dict, AnyStr, List, Optional
import aiohttp
import aiohttp.web as aioweb

class Config:
    """
    Config class
    """
    internal: Optional[Config] = None
    def __init__(self, parallel: bool = True, max_batch: int = 5, proxy_url: Union[AnyStr, List[AnyStr]] = None,
                 max_retries: int = 3, retry_delay: int = 1, max_rand_delay: float = 0.5, min_rand_delay: float = 0.01):
        """
        Do not use init directly, use create method
        """
        self.parallel = parallel
        self.max_batch = max_batch
        self.proxy_url = proxy_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.max_rand_delay = max_rand_delay
        self.min_rand_delay = min_rand_delay

    @classmethod
    def create(cls, *, parallel: bool = True, max_batch: int = 5, proxy_url: Union[AnyStr, List[AnyStr]] = None,
               max_retries: int = 3, retry_delay: int = 1, max_rand_delay: float = 0.5,
               min_rand_delay: float = 0.01) -> Config:
        """
        Sets global settings variable, keywords only
        :param parallel: Controls overlapping of requests
        :param max_batch: Maximum requests active
        :param proxy_url: Set strings according to aiohttp docs
        String or array of strings for random choice of proxy
        :param max_retries: Amount of retries if request fails
        :param retry_delay: Delay between retries
        :param max_rand_delay: Maximum random delay between requests
        :param min_rand_delay: Minimum random delay between requests
        :return: global Config.internal class
        """

        Config.internal = cls(parallel=parallel, max_batch=max_batch, proxy_url=proxy_url, max_retries=max_retries,
                     retry_delay=retry_delay, max_rand_delay=max_rand_delay, min_rand_delay=min_rand_delay)

        return Config.internal

    @property
    def pick_rand_delay(self):
        return uniform(self.min_rand_delay, self.max_rand_delay)

    @property
    def proxy_url(self):
        return self._proxy_url

    @proxy_url.setter
    def proxy_url(self, proxy: Union[AnyStr, List[AnyStr]]):
        if isinstance(proxy, List):
            self._proxy_rand = True
        else:
            self._proxy_rand = False

        self._proxy_url = proxy

    @property
    def proxy(self):
        if self._proxy_rand:
            return choice(self._proxy_url)

        return self._proxy_url

    @property
    def parallel(self):
        return self._parallel

    @parallel.setter
    def parallel(self, value: bool):
        if not value:
            self._lock = Lock()
        else:
            self._lock = None

        self._parallel = value

    @property
    def max_batch(self):
        return self._max_batch

    @max_batch.setter
    def max_batch(self, value: int):
        self._max_batch = value
        self._semaphore_batch = Semaphore(self._max_batch)

    @property
    def lock(self):
        return self._lock

    @property
    def semaphore_batch(self):
        return self._semaphore_batch


Config.create()
