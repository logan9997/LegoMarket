from typing import Any
import time
from django.db.models import Min, Max
from django.http import HttpRequest

def item_type_convert(item_type:str) -> str:
    '''
    Converts item type to alternative format
    '''
    types = {
        'M':'MINIFIG',
        'MINIFIG':'M',
        'S':'SET',
        'SET':'S'
    }

    if item_type not in types.keys():
        raise Exception('Invalid item type')

    return types[item_type]

def metric_convert(metric) -> str:
    metrics = {
        'price_new': 'Price New',
        'price_used':'Price Used',
        'qty_new':'Quantity New',
        'qty_used':'Quantity Used',
    }
    if metric not in metrics.keys():
        return 'Price New'

    return metrics[metric]


def get_current_page(request: HttpRequest, key='pg') -> int:
    '''
    Get current page from request.GET
    '''
    current_page = request.GET.get(key, 1)
    try:
        current_page = int(current_page)
    except:
        current_page = 1
    return current_page


def clean_html_codes(string:str) -> str:
    '''
    Removes html codes from string; e.g. "&#40Anakin Skywalker&#41" -> "(Anakin Skywalker)"
    '''
    codes = {
        '&#41;': ')',
        '&#40;': '(',
        '&#39;': "'"
    }
    for html, char in codes.items():
        if html in string:
            string = string.replace(html, char)
    return string

def timer(func: Any) -> Any:
    '''
    Calculates run time of a function
    '''
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        finish = time.time() - start
        print(f'<{func.__name__}> finished in {round(finish, 5)} seconds.')
        return result
    return wrapper

def get_year_released_limit(limit:Min | Max) -> int:
    from App.models import Item
    year = Item.objects.filter(year_released__gt=0).aggregate(
        year_released=limit('year_released')
    ).get('year_released')
    return int(year)