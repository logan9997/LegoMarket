from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from typing import Any
from ..models import Item, Price
from django.db.models import Subquery, OuterRef, F, DecimalField, Func, Value
from datetime import datetime
from config import DATE_FORMAT


class HomeView(TemplateView):
    template_name = 'App/home/home.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.title = 'Home'
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.get_trending_items()
        context.update({
            'title': self.title,
            'request':self.request,
            'recently_viewed': self.get_recently_viewed_items()
        })
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    def get_recently_viewed_items(self):
        item_ids = self.request.session.get('recently_viewed', [])
        items = Item.objects.filter(item_id__in=item_ids)
        return items
    
    def get_trending_items(self):
        todays_date = datetime.now().strftime(DATE_FORMAT)
        latest_prices = Price.objects.filter(
            date=todays_date, item_id=OuterRef('item_id')
        ).values('price_new')[:1]
        
        percentage_change = (
            (F('price_new') - Subquery(latest_prices)) / F('price_new') * 100
        )     

        result = Price.objects.filter(date='2023-12-11').values(
                'item_id', 
                item_name=F('item__item_name'),
                image_path=F('item__image_path'),
            ).annotate(
                price_new_change=Func(
                    percentage_change,
                    Value(2),
                    function='ROUND',
                    output_field=DecimalField()
                )
            )
        print(result[0].values())