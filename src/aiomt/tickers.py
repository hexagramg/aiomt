import re
from typing import AnyStr
import json
from getter import RequestsFactory
from iframe_helpers import get_iframe_url








class Ticker:
    def __init__(self, ticker: AnyStr):
        self.ticker = ticker
        self.pe_r = None
        self.eps = None

    async def get_pe(self) -> dict:
        if self.pe_r is not None:
            return self.pe_r

        self.pe_r = await self.__get_from_chartdata('pe')
        return self.pe_r

    async def get_eps(self) -> dict:
        if self.eps is not None:
            return self.eps

        self.eps = await self.__get_from_chartdata('eps')
        return self.eps

    async def __get_from_chartdata(self, iframe_type) -> dict:
        if self.pe_r is not None:
            return self.pe_r
        url = get_iframe_url(self.ticker, iframe_type)
        t = await RequestsFactory.get_text(url)
        data_pattern = r'var chartData = (\[.*\])'
        data_extract = re.compile(data_pattern)
        t = data_extract.findall(t)[0]
        t = json.loads(t)
        return t

