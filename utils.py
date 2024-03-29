from typing import Any
import time
from django.db.models import Min, Max
from django.http import HttpRequest, HttpResponse
from config import NO_USER_LOGGED_IN_VALUE, METRICS
from django.shortcuts import redirect

class Chart:

    def __init__(self, request: HttpRequest, item_id: str) -> None:
        from App.models import Price
        self.Price = Price
        self.request = request
        self.item_id = item_id

    def get_selected_chart_metric(self) -> str:
        '''
        Returns and validates the selected chart_metric
        '''
        default_value = 'price_new'
        selected_metric =  self.request.GET.get('chart_metric', default_value)
        if selected_metric not in METRICS:
            return default_value
        return selected_metric
    
    def get_chart_data(self, metric:str) -> list:
        '''
        Returns a list of metrics for selected item to be plotted inside chart
        '''
        metrics = self.Price.objects.filter(
            item_id=self.item_id
        ).values_list(metric, flat=True).order_by('date')
        return list(metrics)
    
    def get_metric_percentage_change(self, metric:str) -> float:
        '''
        Calculates the percentage change between the earliest and latest record
        of the selected item's selected chart metric
        '''
        prices_objects = self.Price.objects.filter(
            item_id=self.item_id
        ).values_list(metric, flat=True)

        earliest = prices_objects.earliest('date') 
        if earliest == 0:
            return 100
        latest = prices_objects.latest('date')

        percentage_change = (earliest - latest) / earliest * -100
        
        if percentage_change == -0:
            percentage_change = 0

        return round(percentage_change, 2)


def get_previous_url(request: HttpRequest, default_value='home') -> str | Any:
    return request.META.get('HTTP_REFERER', default_value)

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
    '''
    Returns either the Min or Max year_released value from models.Item
    '''
    from App.models import Item

    year = Item.objects.filter(
        year_released__gt=0
    ).aggregate(
        year_released=limit('year_released')
    ).get(
        'year_released'
    )
    return int(year)


def get_portfolio_item_inventory(item_id: str, user_id: int) -> list[dict[str, Any]]:
    '''
    Return a list of dicts containing;

    dict['form'] = PortfolioItem form object, with initial values set from 
    items retrived from database 

    dict['entry_id'] = entry_id for each Portfolio object    
    '''

    from App.forms import PortfolioItem
    from App.models import Portfolio

    initial_values = Portfolio.objects.filter(
        item_id=item_id, 
        user_id=user_id
    ).values(
        'bought_for',
        'date_acquired',
        'notes',
        'entry_id'
    ).order_by(
        '-entry_id'
    )

    forms = []
    for values in initial_values:
        entry_id = values.pop('entry_id')
        data = {
            'form': PortfolioItem(initial=values),
            'entry_id': entry_id
        }
        forms.append(data)
        
    return forms


def get_signup_error(error: str):
    if 'duplicate key' in error:
        if 'username' in error:
            return 'username already exists'
        elif 'email' in error:
            return 'email already exists'
    return 'Error signing up'    


class AuthenticatedUserNotAllowed:
    '''
    Don't allow authenticated users to visit a view
    '''
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            previous_url = get_previous_url(request)
            return redirect(previous_url)
        return super().dispatch(request, *args, **kwargs)