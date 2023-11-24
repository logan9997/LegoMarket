from django import http
from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView, FormView
from ..models import Item, Price
from ..forms import MetricLimits
from typing import Any
from django.http import QueryDict

def search_form_handler(request: HttpRequest):
    if request.method == 'GET':
        form = MetricLimits(request.GET)
        if form.is_valid():
            params = QueryDict(mutable=True)
            for k,v in form.cleaned_data.items():
                if v != 0:
                    params[k] = v
            params = params.urlencode()

            if params != '':
                return redirect('search/?' + params)
            
    return redirect('search/')


class SearchView(TemplateView):
    template_name = 'App/search/search.html'    

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.title = 'Search'
        self.request = request
        self.form = MetricLimits(initial={
            field: request.GET.get(field, 0) for field in MetricLimits().fields
        })
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'items':self.get_items(),
            'forms': self.form
        })
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    def get_items(self, orders=('item_type', 'item_id'), filters={}):
        items = Item.objects.filter(**filters).order_by(*orders)
        return items
        
