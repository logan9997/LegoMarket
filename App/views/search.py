from django import http
from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView, View
from ..models import Item, Price
from ..forms import MetricLimits
from config import ITEMS_PER_PAGE
from typing import Any
from django.db.models import Q, F
from utils import get_current_page
import math

class SearchFormHandler(View):

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        previous_url_params = self.get_previous_url_params()
        new_params = self.get_new_params()
        params = self.join_params(previous_url_params, new_params)
        params = self.filter_out_params(params)
        params_string = params.urlencode()
        return redirect('search/?' + params_string)
    
    def get_previous_url_params(self):
        previous_url:str = self.request.META['HTTP_REFERER']
        params = None
        if '?' in previous_url:
            params = previous_url.split('?')[1]
        params = QueryDict(params, mutable=True)
        return params
    
    def params_string(self, params: dict):
        return '&'.join([f'{k}={v}' for k, v in params.items()])

    def get_new_params(self):
        metric_limits = MetricLimits(self.request.GET, request=self.request)
        if metric_limits.is_valid():
            data:dict = metric_limits.cleaned_data
            params_string = self.params_string(data)
            params = QueryDict(params_string, mutable=True)  
        return params

    def join_params(self, p1: dict, p2: dict):
        p2.update(p1)
        params = dict(p2)
        for k, v in params.items():
            params[k] = v[0]
        params = self.params_string(params)
        params = QueryDict(params)
        return params
    
    def filter_out_params(self, params: QueryDict):
        new_params = QueryDict(mutable=True)
        for k, v in params.items():
            if v != '0' or v.isalnum():
                new_params[k] = v
        return new_params


class SearchView(TemplateView):
    template_name = 'App/search/search.html'    

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.title = 'Search'
        self.request = request
        self.query = request.GET.get('q', '')
        self.filters = self.get_metric_filters()
        self.items = self.get_items(self.query, filters=self.filters)
        self.last_page = math.ceil(len(self.items) / ITEMS_PER_PAGE)
        self.current_page = self.validate_current_page(get_current_page(request))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'items': self.items[(self.current_page - 1) * ITEMS_PER_PAGE : self.current_page * ITEMS_PER_PAGE],
            'current_page': self.current_page,
            'query': self.query,
            'last_page': self.last_page,
            'forms': {
                'filters': MetricLimits(request=self.request)
            }
        })
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
    
    def get_items(self, query, orders=('item_id', 'item_type'), filters={}):
        items = Item.objects.filter(
            Q(item_id__icontains=query) | Q(item_name__icontains=query), 
            **filters
        ).order_by(*orders).values(
            'item_id',
            'item_name',
            'item_type',
            'image_path',
            price_used=F('price__price_used'),
            price_new=F('price__price_new'),
            qty_used=F('price__qty_used'),
            qty_new=F('price__qty_new'),
        ).distinct('item_id')
        return items
    
    def get_metric_filters(self):
        filtered_metrics = {
            k: v for k, v in self.request.GET.items() 
            if 'min' in k or 'max' in k
        }
        filters = {}
        for k, v in filtered_metrics.items():
            metric = k[4:]
            if 'min' in k:
                filters[f'price__{metric}__gte'] = v
            else:
                filters[f'price__{metric}__lte'] = v
        return filters
    
    def validate_current_page(self, current_page) -> int:
        try:
            current_page = int(current_page)
        except:
            return 1
        if current_page > self.last_page and self.last_page != 0:
            current_page = self.last_page
        elif current_page <= 0:
            current_page = 1
        return current_page
