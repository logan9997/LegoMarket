DATE_FORMAT = '%Y-%m-%d'
METRICS = ['price_new', 'price_used', 'qty_new', 'qty_used']

class ModelsConfig:

    class Length:
        ITEM_ID = 50
        ITEM_NAME = 300
        ITEM_TYPE = 1
        USERNAME = 16
        PASSWORD = 20
        IMAGE_PATH = 400

    class Decimal:
        MAX_DIGITS = 10
        DECIMAL_PLACE = 2

    class Choice:
        ITEM_TYPE = (('S', 'S'), ('M', 'M'))