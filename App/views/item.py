from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView
from ..models import Item, Price
from typing import Any
from decimal import Decimal
from ..forms import chartMetricSelect
from fuzzywuzzy import fuzz
from utils import timer
from config import METRICS

class ItemView(TemplateView):
    template_name = 'App/item/item.html'

    def dispatch(self, request: HttpRequest, item_id:str, *args: Any, **kwargs: Any) -> HttpResponse:
        self.item_id = item_id
        if not self.is_item_id_valid():
            return redirect('home')
        self.title = f'Item/{self.item_id}'
        self.selected_chart_metric = self.get_selected_chart_metric()
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    @timer
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        chart_metrics = self.get_chart_data(self.selected_chart_metric)

        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'item_info': self.get_item_info(),
            'chart_metric':self.get_selected_chart_metric(),
            'chart_metrics': chart_metrics,
            'chart_dates': self.get_chart_data('date'),
            'metric_difference':chart_metrics[-1] - chart_metrics[0],
            'metric_percentage_difference':self.get_metric_percentage_change(self.selected_chart_metric),
            'chart_id':f'chart-{self.item_id}',
            'price_new': self.get_current_metric('price_new'),
            'price_used': self.get_current_metric('price_used'),
            'qty_new': self.get_current_metric('qty_new'),
            'qty_used': self.get_current_metric('qty_used'),
            'similar_items': self.get_similar_items(),
            'form':chartMetricSelect,
        })
        return context
    
    def is_item_id_valid(self) -> bool:
        item_ids = Item.objects.all().values_list('item_id', flat=True)
        if self.item_id in item_ids:
            return True
        return False

    def get_selected_chart_metric(self) -> str:
        default_value = 'price_new'
        selected_metric =  self.request.GET.get('chart_metric', default_value)
        if selected_metric not in METRICS:
            return default_value
        return selected_metric
    
    def get_item_info(self):
        return Item.objects.get(item_id=self.item_id)
        
    def get_chart_data(self, metric:str):
        metrics = Price.objects.filter(
            item_id=self.item_id
        ).values_list(metric, flat=True).order_by('date')
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

        percentage_change = (latest - earliest) / latest * 100
        return round(percentage_change, 2)

    def get_similar_items(self):
        threshold = 90
        threshold_stop_limit = 60
        similar_items_limit = 6
        threshold_decrement = 5

        selected_item = self.get_item_info()
        items = Item.objects.filter(
            item_type=selected_item.item_type
        ).values('item_id','item_name').exclude(item_name=selected_item.item_name)

        similar_items = []
        while True:
            for item in items:
                if fuzz.partial_ratio(selected_item.item_name, item['item_name']) >= threshold:
                    similar_item = Item.objects.get(item_id=item['item_id'])
                    similar_items.append(similar_item)
                    items = items.exclude(item_id=similar_item.item_id)

            if len(similar_items) >= similar_items_limit or threshold <= threshold_stop_limit:
                similar_items = similar_items[:similar_items_limit]
                return similar_items
            
            threshold -= threshold_decrement
