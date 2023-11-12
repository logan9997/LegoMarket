from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponse, redirect
from ..forms import SearchItem
from ..models import Item


def search_form(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SearchItem(request.POST)
        if form.is_valid():
            search_value = form.cleaned_data.get('search_value')
            item_ids = Item.objects.all().values_list('item_id', flat=True)
            if search_value in item_ids:
                return redirect(f'item/{search_value}')
    previous_url = request.META.get('HTTP_REFERER', 'home')
    return redirect(previous_url)
