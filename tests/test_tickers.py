import pytest
import aiomt
import asyncio

loop = asyncio.get_event_loop()


def test_get_pe_ratios():
    ticker = aiomt.Ticker('msft')
    data = loop.run_until_complete(ticker.get_pe())
    assert data


def test_get_eps():
    ticker = aiomt.Ticker('goog')
    data = loop.run_until_complete(ticker.get_eps())
    assert data
