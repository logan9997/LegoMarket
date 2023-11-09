DATE_FORMAT = '%Y-%m-%d'

class ModelsConfig:

    class Length:
        ITEM_ID = 50
        ITEM_NAME = 300
        ITEM_TYPE = 1
        USERNAME = 16
        PASSWORD = 20

    class Decimal:
        MAX_DIGITS = 10
        DECIMAL_PLACE = 2

    class Choice:
        ITEM_TYPE = (('S', 'S'), ('M', 'M'))