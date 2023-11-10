from django.http import HttpRequest
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from ..models import Item, Price
from typing import Any
from decimal import Decimal
from fuzzywuzzy import fuzz


class ItemView(TemplateView):
    template_name = 'App/item/item.html'

    def dispatch(self, request:HttpRequest, item_id:str, *args, **kwargs) -> HttpResponse:
        self.item_id = item_id
        self.title = f'Item/{self.item_id}'
        self.selected_graph_metric = 'price_new'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'item_info': self.get_item_info(),
            'graph_metrics': self.get_graph_metrics(self.selected_graph_metric),
            'price_new': self.get_current_metric('price_new'),
            'price_used': self.get_current_metric('price_used'),
            'qty_new': self.get_current_metric('qty_new'),
            'qty_used': self.get_current_metric('qty_used'),
            'similar_items': self.get_similar_items()
        })
        self.get_similar_items()
        return context
    
    def get_item_info(self):
        return Item.objects.get(item_id=self.item_id)
    
    def get_graph_metrics(self, metric:str):
        metrics = Price.objects.filter(
            item_id=self.item_id
        ).values('date', metric).order_by('-date')
        return metrics
    
    def get_current_metric(self, metric:str) -> Decimal | int:
        metric = Price.objects.filter(
            item_id=self.item_id
        ).values_list(metric, flat=True).latest('date')
        return metric
    
    def get_similar_items(self):
        threshold = 75
        selected_item_name = self.get_item_info().item_name
        item_names = Item.objects.all().values_list('item_name', flat=True)
        similar_items = [
            Item.objects.filter(item_name=item_name) 
            for item_name in item_names 
            if fuzz.partial_ratio(selected_item_name, item_name) >= threshold
        ]
        return similar_items