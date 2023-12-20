from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from typing import Any
from ..models import Item, Price
from django.db.models import Subquery, OuterRef, F, DecimalField, Func, Value, ExpressionWrapper, Max
from django.db.models.manager import BaseManager
from utils import timer
from config import DATE_FORMAT
from datetime import datetime, timedelta
from decimal import Decimal

class HomeView(TemplateView):
    template_name = 'App/home/home.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.title = 'Home'
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'request':self.request,
            'recently_viewed': self.get_recently_viewed_items(),
            'trending_items': self.get_trending_items()
        })
        return context
    
    def get_recently_viewed_items(self) -> BaseManager[Item]:
        '''
        Returns items which the user has recently visited their item profile 
        page. Recently viewed item_ids stored inside request.session
        '''
        item_ids = self.request.session.get('recently_viewed', [])
        items = [Item.objects.filter(item_id=item_id)[0] for item_id in item_ids]
        return items
    
    def get_trending_items(self) -> BaseManager[Price]:
        '''
        Returns items with the biggest percentage change in price in the last 
        7 days
        '''
        latest_prices = Price.objects.filter(
            item_id=OuterRef('item_id')
        ).order_by('-date').values('price_new')[:1]

        percentage_change = (F('price_new') - Subquery(latest_prices)) / F('price_new') * -100

        order_by_expression = Func(
            F('price_change'),
            function='ABS',
            output_field=DecimalField()
        )

        last_weeks_date = datetime.now() - timedelta(days=7)
        last_weeks_date = last_weeks_date.strftime(DATE_FORMAT)

        result = Price.objects.filter(
            date=last_weeks_date, price_new__gt=0
        ).values(
            'item_id',
            item_name=F('item__item_name'),
            image_path=F('item__image_path'),
        ).annotate(
            price_change=ExpressionWrapper(
                Func(
                    percentage_change,
                    Value(2),
                    function='ROUND',
                    output_field=DecimalField()
                ), 
                output_field=DecimalField()
            )
        ).order_by(
            order_by_expression.desc()
        )[:10]
        return result