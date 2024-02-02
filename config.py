DATE_FORMAT = '%Y-%m-%d'
SEARCH_ITEMS_PER_PAGE = 18
MAX_RECENTLY_VIEWED_ITEMS = 8
NO_USER_LOGGED_IN_VALUE = -1

class ModelsConfig:

    class Length:
        ITEM_ID = 50
        ITEM_NAME = 300
        ITEM_TYPE = 1
        USERNAME = 16
        PASSWORD = 20
        IMAGE_PATH = 400
        NOTES = 300

    class Decimal:
        MAX_DIGITS = 10
        DECIMAL_PLACE = 2

    class Choice:
        ITEM_TYPE = (('S', 'S'), ('M', 'M'))


class Input:

    PAGE_BUTTON_INPUTS = [
        # {'name':'first', 'value': '<<'},
        {'name':'previous', 'value': '<', 'direction' : -1},
        {'name':'next', 'value': '>', 'direction': 1},
        # {'name':'last', 'value': '>>'},
    ]

METRICS = ['price_new', 'price_used', 'qty_new', 'qty_used']