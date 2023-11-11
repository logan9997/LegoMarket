from django import template
from ..models import Item
from ..forms import SearchItem

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
