BASE_URL = 'https://www.etp-ets.ru/'  # Базовый URL
PARSE_URL = BASE_URL + '44/catalog/procedure'  # URL для основного парсинга
MAX_PRICE_URL = PARSE_URL + '?order=contract_start_price&dir=desc'  # URL для парсинга максимальной цены

PRICE_STEP = 100  # Шаг цены (для создания диапазонов цен тендеров для парсинга)
PRICE_CORR = 0.01  # Корректировка начальной цены (для исключения попадания спарсеных тендеров в выборку)
TENDERS_LIMIT = 100  # Ограничение количества тендеров на страницу (Доступные варианты: 10, 25, 75, 100)

DATETIME_FORMAT = '%d.%m.%Y %H:%M'  # Формат для преобразования извлекаемых дат тендера
