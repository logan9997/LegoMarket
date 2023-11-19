from django import template
from ..models import Item
from ..forms import SearchItem
from utils import (
    item_type_convert as _item_type_convert, 
    metric_convert as _metric_convert
)

register = template.Library()

@register.simple_tag
def get_item_search_form():
    return SearchItem()

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
