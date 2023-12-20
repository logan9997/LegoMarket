from django import template
from django.http import HttpRequest
import locale
from decimal import Decimal
from ..models import Item, User
from ..forms import SearchItem
from utils import (
    item_type_convert as _item_type_convert, 
    metric_convert as _metric_convert
)

register = template.Library()

@register.simple_tag(takes_context=True)
def get_username(context):
    request = context['request']
    user_id = request.session.get('user_id', 1)
    try:
        user = User.objects.get(user_id=user_id)
    except:
        return 'Guest'
    return user.username

@register.simple_tag(takes_context=True)
def logged_in(context: dict) -> bool:
    request = context['request']
    user_id = request.session.get('user_id', -1)
    if user_id == -1:
        return False
    return True

@register.simple_tag(takes_context=True)
def get_pages_qstring(context):
    request:HttpRequest = context['request']
    params = request.GET
    params._mutable = True
    if 'pg' in params:
        params.pop('pg')
    return params.urlencode()

@register.simple_tag(takes_context=True)
def get_item_search_form(context):
    request = context['request']
    return SearchItem(request)


@register.simple_tag
def get_item_names():
    item_names = Item.objects.all().values_list(
        'item_name', flat=True
    ).order_by('item_id')
    return list(item_names)


@register.simple_tag
def get_item_ids():
    item_ids = Item.objects.all().values_list(
        'item_id', flat=True
    ).order_by('item_id')
    return list(item_ids)


@register.filter
def item_type_convert(item_type:str, string_method:str):
    return getattr(_item_type_convert(item_type), string_method)()


@register.filter
def metric_convert(metric: str):
    return _metric_convert(metric)


@register.filter
def index(iterable, index:int):
    return iterable[index]


@register.filter
def add_sign(number):
    if number >= 0:
        return f'+{number}'
    return number


@register.filter
def insert(iterable, char_and_index:str):
    char = char_and_index.split(',')[0]
    index = int(char_and_index.split(',')[1])
    iterable = list(str(iterable))
    iterable.insert(index, char)
    return ''.join(iterable)


@register.filter
def add(num1, num2) -> int:
    return num1 + num2


@register.filter
def skip_index(iterable, index:int):
    print(iterable, index)
    return iterable[index:]


@register.filter
def format_number(number):
    locale.setlocale(locale.LC_ALL, '')
    if type(number) == Decimal:
        formatted_number = locale.format_string(
            "%.*f", 
            (locale.localeconv()['frac_digits'], number), 
            grouping=True
        )
    else:
        formatted_number = locale.format("%d", number, grouping=True)
    return formatted_number