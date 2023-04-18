BASE_URL = 'https://www.etp-ets.ru/'
PARSE_URL = BASE_URL + '44/catalog/procedure'
PRICE_SORT_URL = '?order=contract_start_price&dir='
MAX_PRICE_URL = PRICE_SORT_URL + 'desc'
MIN_PRICE_URL = PRICE_SORT_URL + 'asc'

PRICE_STEP = 0.5
DATETIME_FORMAT = '%d.%m.%Y %H:%M'
