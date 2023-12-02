from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView, View
from ..models import Item, Price
from ..forms import MetricLimits, ItemType, YearReleased, Order
from config import ITEMS_PER_PAGE
from typing import Any
from django.db.models import Q, F, Subquery, OuterRef
from utils import get_current_page
import math
from django import forms

class Filters:

    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def order(self):
        order = self.request.GET.get('order')
        print('ORDER!!', order)
        if order != None:
            return (f'price__{order}', )
        return ()

    def get_metric_filters(self) -> dict:
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
    
    def get_item_type_filter(self) -> dict:
        filters = {}
        if self.request.GET.get('item_type') in ['S', 'M']:
            filters['item_type'] = self.request.GET['item_type']
        return filters

    def get_year_released_filter(self) -> dict:
        filters = {}
        year_released = self.request.GET.get('year_released')
        if year_released != None:
            filters['year_released'] = year_released
        return filters
    
    def filters(self) -> dict:
        filters = {}
        get_filter_methods = [m for m in dir(self) if m[:3] == 'get']
        for method in get_filter_methods:
            filters.update(getattr(self, method)())
        return filters

class SearchFormHandler(View):

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        self.forms:dict[str, forms.Form] = {
            'metric_limits': MetricLimits(request.GET, request=self.request),
            'item_type': ItemType(request.GET),
            'year_released':YearReleased(request.GET),
            'order': Order(request.GET)
        }
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
        form_name = self.request.GET.get('form_name')
        form = self.forms.get(form_name)
        if form.is_valid():
            data:dict = form.cleaned_data
            params_string = self.params_string(data)
            params = QueryDict(params_string, mutable=True)  
            return params
        return QueryDict()

    def join_params(self, previous_params: dict, new_params: dict):
        new_params.update(previous_params)
        params = dict(new_params)
        for k, v in params.items():
            params[k] = v[0]
        params = self.params_string(params)
        params = QueryDict(params)
        return params
    
    def filter_out_params(self, params: QueryDict):
        new_params = QueryDict(mutable=True)
        for k, v in params.items():
            if v not in ['0', 'None'] and k != 'form_name':
                new_params[k] = v
        return new_params


class SearchView(TemplateView):
    template_name = 'App/search/search.html'    

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.title = 'Search'
        self.request = request
        self.query = request.GET.get('q', '')
        self.filters = Filters(request).filters()
        self.order = Filters(request).order()
        self.items = self.get_items(self.query, filters=self.filters, orders=self.order)
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
                'filters': MetricLimits(request=self.request),
                'item_type': ItemType(),
                'year_released': YearReleased(),
                'order': Order()
            }
        })
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
    
    def get_items(self, query, orders=('item_id', 'item_type'), filters={}):
        latest_date_query = Price.objects.filter(
            item=OuterRef('item_id')
        ).order_by('-date').values('date')[:1]

        items = Price.objects.select_related('item').annotate(
            latest_date=Subquery(latest_date_query)
        ).values(
            'price_used',
            'price_new',
            'qty_used',
            'qty_new', 
            'item_id',
            item_name=F('item__item_name'),
            item_type=F('item__item_type'),
            image_path=F('item__image_path'), 
            year_released=F('item__year_released')        
        ).filter(
            Q(item__item_id__icontains=query) | Q(item_name__icontains=query),
            date=F('latest_date'), **filters
        )
        return items

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
