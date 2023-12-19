from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView, View
from ..models import Price
from ..forms import YearReleased, ItemType, MetricLimits, Order
from config import ITEMS_PER_PAGE
from typing import Any
from django.db.models import Q, F, Subquery, OuterRef
from utils import get_current_page
import math
from decimal import Decimal
from django import forms

class FormHandler(View):

    def __init__(self):
        self.invalid_values = [0, '0', Decimal(0), None]
        self.forms = {
            'year_released': YearReleased,
            'item_type': ItemType,
            'metric_limits': MetricLimits,
            'order': Order
        }

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        qstring = self.get_qstring()
        host = self.request.get_host()
        return redirect(f'http://{host}/search/?{qstring}')
        
    def get_form(self) -> forms.Form:
        form_name = self.request.GET.get('form_name')
        form = self.forms.get(form_name)
        return form(self.request.GET)
    
    def qstring(self, params:dict[str, str]) -> str:
        '''
        Constricts a query string of given parameters defined inside params. e.g. foo=1&bar=2
        '''
        qstring = '&'.join([f'{k}={v}' for k, v in params.items()])
        return qstring

    def get_current_params(self) -> QueryDict:
        '''
        Gets parmaters from url before FormHandler is called.
        '''
        previous_url:str = self.request.META.get('HTTP_REFERER')
        if '?' in previous_url:
            current_params = previous_url.split('?')[1]
            current_params = QueryDict(current_params, mutable=True)
            if 'clear' in self.form.data:
                current_params = self.clear(current_params)
            return current_params
        return QueryDict()

    def get_new_params(self) -> QueryDict:
        '''
        Gets parameters passed from submitted form
        '''
        if self.form.is_valid() and 'clear' not in self.form.data:
            data:dict = self.form.cleaned_data
            data.pop('form_name')
            new_params = self.qstring(data)
            return QueryDict(new_params)
        return QueryDict()
    
    def validate_params(self, params: QueryDict) -> QueryDict:
        '''
        Creates new QueryDict and does not assign invalid values from 
        the submitted form
        '''
        valid_params = QueryDict(mutable=True)
        for k, v in params.items():
            if v not in self.invalid_values and k != 'clear':
                valid_params[k] = v
        return valid_params
    
    def clear(self, params: QueryDict) -> QueryDict:
        '''
        Clears parameters from params QueryDict which are also present 
        inside a forms fields if a forms clear button is clicked
        '''
        fields = self.form.fields
        for field in fields:
            if field in params.keys():
                params.pop(field)
        return params

    def join_params(self, current:QueryDict, new:QueryDict) -> QueryDict:
        '''
        Combines two QueryDicts together
        '''
        current._mutable = True
        for k, v in new.items():
            current[k] = v
        return current
    
    def get_qstring(self) -> str:
        '''
        Returns query string based off of parameters submitted from the 
        current form, as well as parameters found inside the previous URL 
        '''
        self.form = self.get_form()
        current_params = self.get_current_params()
        new_params = self.get_new_params()
        params = self.join_params(current_params, new_params)
        params = self.validate_params(params)
        qstring = params.urlencode()
        return qstring

    
class Filters:

    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def year_released(self) -> dict[str, str] | dict:
        '''
        Returns year_released value from URL
        '''
        year_released = self.request.GET.get('year_released')
        if year_released:
            return {'year_released': year_released}
        return {}
    
    def item_type(self) -> dict[str, str] | dict:
        '''
        Returns item_type value from URL
        '''
        item_type = self.request.GET.get('item_type', 'All')
        if item_type != 'All':
            return {'item_type': item_type}
        return {}
    
    def metrics_limits(self) -> dict[str, str] | dict:
        '''
        Returns metric_limits value(s) from URL
        '''
        filtered_metrics = {
            k: v for k, v in self.request.GET.items() 
            if 'min' in k or 'max' in k
        }
        filters = {}
        for k, v in filtered_metrics.items():
            metric = k[4:]
            if 'min' in k:
                filters[f'{metric}__gte'] = v
            else:
                filters[f'{metric}__lte'] = v
        return filters

    def get_order(self) -> str:
        '''
        Returns order value from URL; defualt value = 'item_id'
        '''
        order = self.request.GET.get('order', 'item_id')
        return order
    
    def get_filters(self) -> dict[str, str]:
        '''
        Returns a dict of all filters found inside the URL to be used as the 
        filters parameter inside SearchView.get_items()
        '''
        filters = {}
        get_filters = [self.year_released, self.item_type, self.metrics_limits]
        for method in get_filters:
            filters.update(method())
        return filters

class SearchView(TemplateView):
    template_name = 'App/search/search.html'    

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.forms = {
            'year_released': YearReleased(initial=YearReleased.set_initial(request)),
            'item_type': ItemType(initial=ItemType.set_initial(request)),
            'metric_limits': MetricLimits(initial=MetricLimits.set_initial(request)),
            'order': Order(initial=Order.set_initial(request))
        }
        self.title = 'Search'
        self.request = request
        self.query = request.GET.get('q', '')
        self.filters = Filters(request).get_filters()
        self.order = Filters(request).get_order()
        self.items = self.get_items(self.query, filters=self.filters, orders=self.order)
        self.last_page = math.ceil(len(self.items) / ITEMS_PER_PAGE)
        self.current_page = self.validate_current_page(get_current_page(request))
        self.shown_items = self.items[
            (self.current_page - 1) * ITEMS_PER_PAGE : self.current_page * ITEMS_PER_PAGE
        ]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'shown_items': self.shown_items,
            'items_count': len(self.items),
            'current_page': self.current_page,
            'query': self.query,
            'last_page': self.last_page,
            'forms': self.forms
        })
        return context
    
    def get_items(self, query, orders=('item_id'), filters={}):
        '''
        Returns items based off of search parameters
        '''
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
            date=F('latest_date'), 
            **filters
        ).order_by(orders)
        return items

    def validate_current_page(self, current_page: Any) -> int:
        '''
        Validates the current page number if current_page is not of 
        type int & current_page <= 0 & current_page > self.last_page 
        '''
        try:
            current_page = int(current_page)
        except:
            return 1
        if current_page > self.last_page and self.last_page != 0:
            current_page = self.last_page
        elif current_page <= 0:
            current_page = 1
        return current_page
