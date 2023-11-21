from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView
from ..models import Item, Price
from ..forms import MetricLimits
from typing import Any

class SearchView(TemplateView):
    template_name = 'App/search/search.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.title = 'Search'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'items':self.get_items(),
            'forms': MetricLimits()
        })
        return context

    def get_items(self, orders=('item_type', 'item_id'), filters={}):
        items = Item.objects.filter(**filters).order_by(*orders)
        return items
    