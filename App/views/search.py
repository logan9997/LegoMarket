from django import http
from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView, View
from ..models import Item, Price
from ..forms import YearReleased
from config import ITEMS_PER_PAGE
from typing import Any
from django.db.models import Q, F, Subquery, OuterRef
from utils import get_current_page
import math

class FormHandler(View):

    def __init__(self) -> None:
        self.forms = {
            'year_released': YearReleased
        }

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        current_params = self.get_current_params()
        new_params = self.get_new_params()
        params = self.join_params(current_params, new_params)
        qstring = params.urlencode()
        host = self.request.get_host()
        return redirect(f'http://{host}/search/?{qstring}')
    
    def qstring(self, params:dict[str, str]) -> str:
        qstring = '&'.join([f'{k}={v}' for k, v in params.items()])
        return qstring

    def get_current_params(self) -> str:
        previous_url:str = self.request.META.get('HTTP_REFERER')
        if '?' in previous_url:
            current_params = previous_url.split('?')[1]
            return QueryDict(current_params)
        return QueryDict()

    def get_new_params(self) -> str:
        form_name = self.request.GET.get('form_name')
        form = self.forms.get(form_name)
        form = form(self.request.GET)
        if form.is_valid():
            data:dict = form.cleaned_data
            data.pop('form_name')
            new_params = self.qstring(data)
            return QueryDict(new_params)
        return QueryDict()
    
    def join_params(self, current:QueryDict, new:QueryDict) -> QueryDict:
        current._mutable = True
        for k, v in new.items():
            current[k] = v
        return current

    
class SearchView(TemplateView):
    template_name = 'App/search/search.html'    

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.title = 'Search'
        self.request = request
        self.query = request.GET.get('q', '')
        self.filters = {}
        self.order = ()
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
                'year_released': YearReleased
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
