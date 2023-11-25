from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView
from ..models import Item
from ..forms import MetricLimits
from config import ITEMS_PER_PAGE
from typing import Any
from django.db.models import Q
from utils import get_current_page

def search_form_handler(request: HttpRequest):
    return redirect('search/')


class SearchView(TemplateView):
    template_name = 'App/search/search.html'    

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.title = 'Search'
        self.query = request.GET.get('q', '')
        self.items = self.get_items(self.query)
        self.current_page = get_current_page(request)
        self.last_page = round(len(self.items) / ITEMS_PER_PAGE)
        self.current_page = self.validate_current_page()
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'items': self.items[self.current_page * ITEMS_PER_PAGE : (self.current_page + 1) * ITEMS_PER_PAGE],
            'current_page': self.current_page,
            'query': self.query,
            'last_page': self.last_page,
            'forms': {
                'filters': MetricLimits(initial={
                    field: self.request.GET.get(field, 0) for field in MetricLimits().fields
                })
            }
        })
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
    
    def get_items(self, query, orders=('item_type', 'item_id'), filters={}):
        items = Item.objects.filter(
            Q(item_id__icontains=query) | Q(item_name__icontains=query), **filters
        ).order_by(*orders)
        return items
    
    def validate_current_page(self) -> None:
        try:
            current_page = int(self.current_page)
        except:
            return 1
        if current_page <= 0:
            current_page = 1
        elif current_page > self.last_page:
            current_page = self.last_page
        return current_page
