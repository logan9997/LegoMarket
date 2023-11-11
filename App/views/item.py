from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from ..models import Item, Price
from typing import Any
from decimal import Decimal
from ..forms import GraphMetricSelect
from fuzzywuzzy import fuzz


class ItemView(TemplateView):
    template_name = 'App/item/item.html'

    def dispatch(self, request: HttpRequest, item_id, *args: Any, **kwargs: Any) -> HttpResponse:
        self.item_id = item_id
        self.title = f'Item/{self.item_id}'
        self.selected_graph_metric = self.get_selected_graph_metric()
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'item_info': self.get_item_info(),
            'graph_metrics': self.get_graph_data(self.selected_graph_metric),
            'graph_dates': self.get_graph_data('date'),
            'graph_id':f'graph-{self.item_id}',
            'price_new': self.get_current_metric('price_new'),
            'price_used': self.get_current_metric('price_used'),
            'qty_new': self.get_current_metric('qty_new'),
            'qty_used': self.get_current_metric('qty_used'),
            'similar_items': self.get_similar_items(),
            'form':GraphMetricSelect,
        })
        return context
    
    def get_selected_graph_metric(self) -> str:
        return self.request.GET.get('metric_select', 'price_new')
    
    def get_item_info(self):
        return Item.objects.get(item_id=self.item_id)
    
    def get_graph_data(self, metric:str):
        metrics = Price.objects.filter(
            item_id=self.item_id
        ).values_list(metric, flat=True).order_by('-date')
        return list(metrics)
    
    def get_current_metric(self, metric:str) -> Decimal | int:
        metric = Price.objects.filter(
            item_id=self.item_id
        ).values_list(metric, flat=True).latest('date')
        return metric
    
    def get_metric_percentage_change(self, metric:str) -> float:
        prices_objects = Price.objects.filter(
            item_id=self.item_id
        ).values_list(metric, flat=True)

        earliest = prices_objects.earliest('date') 
        if earliest == 0:
            return 100
        latest = prices_objects.latest('date')

        percentage_change = (earliest - latest) / earliest * 100
        return percentage_change

    def get_similar_items(self):
        threshold = 75
        selected_item_name = self.get_item_info().item_name
        item_names = Item.objects.all().values_list(
            'item_name', flat=True
        ).exclude(item_name=selected_item_name)

        similar_items = [
            Item.objects.filter(item_name=item_name) 
            for item_name in item_names 
            if fuzz.partial_ratio(selected_item_name, item_name) >= threshold
        ]
        return similar_items