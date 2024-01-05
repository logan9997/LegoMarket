from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView
from ..models import Item, Price, Portfolio
from typing import Any
from decimal import Decimal
from ..forms import chartMetricSelect, PortfolioItem
from utils import get_user_id
from fuzzywuzzy import fuzz
from config import METRICS, MAX_RECENTLY_VIEWED_ITEMS
from utils import get_portfolio_item_inventory, Chart


class ItemView(TemplateView):
    template_name = 'App/item/item.html'

    def dispatch(self, request: HttpRequest, item_id:str, *args: Any, **kwargs: Any) -> HttpResponse:
        self.item_id = item_id
        self.user_id = get_user_id(request)
        if not self.item_id_valid():
            return redirect('home')
        self.chart = Chart(request, item_id)
        self.title = f'Item/{self.item_id}'
        self.selected_chart_metric = self.chart.get_selected_chart_metric()
        self.request = request
        self.update_recently_viewed_items()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        chart_data = self.chart.get_chart_data(self.selected_chart_metric)

        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'item_info': self.get_item_info(),
            'price_new': self.get_current_metric('price_new'),
            'price_used': self.get_current_metric('price_used'),
            'qty_new': self.get_current_metric('qty_new'),
            'qty_used': self.get_current_metric('qty_used'),
            'similar_items': self.get_similar_items(),
            'portfolio_item_inventory': get_portfolio_item_inventory(self.item_id, self.user_id),
            'chart': {
                'metric':self.chart.get_selected_chart_metric(),
                'data': chart_data,
                'labels': self.chart.get_chart_data('date'),
                'metric_difference':chart_data[-1] - chart_data[0],
                'metric_percentage_difference':self.chart.get_metric_percentage_change(self.selected_chart_metric),
            },
            'forms': {
                'chart_metric_select': chartMetricSelect,
                'portfolio_item': PortfolioItem
            },
        })
        return context
             
    def item_id_valid(self) -> bool:
        '''
        Validates the item_id passed inside the URL, checks if it exists inside 
        database
        '''
        item_ids = Item.objects.all().values_list('item_id', flat=True)
        if self.item_id in item_ids:
            return True
        return False

    def get_item_info(self) -> Item:
        return Item.objects.get(item_id=self.item_id)
        
    def get_current_metric(self, metric:str) -> Decimal | int:
        '''
        Returns the selected metric for todays date, for selected item
        '''
        metric = Price.objects.filter(
            item_id=self.item_id
        ).values_list(metric, flat=True).latest('date')
        return metric
    
    def get_similar_items(self) -> list:
        '''
        Returns a list of items with a similar item name to the selected item's name
        '''
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

    def update_recently_viewed_items(self) -> None:
        '''
        Inserts item_id into request.session.recently_viewed: list
        '''
        item_ids:list[str] = self.request.session.get('recently_viewed', [])
        
        if self.item_id in item_ids:
            item_ids.remove(self.item_id)

        item_ids.insert(0, self.item_id) 

        if len(item_ids) > MAX_RECENTLY_VIEWED_ITEMS:
            item_ids.pop(-1)

        self.request.session['recently_viewed'] = item_ids
        self.request.session.modified = True