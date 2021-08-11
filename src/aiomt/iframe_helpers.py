from typing import AnyStr


base = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?'

param_helper = {
    'eps': ('type=eps-earnings-per-share-diluted', 'statement=income-statement', 'freq=Q'),
    'pe': ('type=pe-ratio', 'statement=price-ratios', 'freq=Q')
}
def get_iframe_url(ticker:AnyStr, type: AnyStr):
    tick_p = f't={ticker}'
    return base + '&'.join((tick_p,) + param_helper[type])