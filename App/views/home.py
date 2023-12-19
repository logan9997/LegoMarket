from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from typing import Any
from ..models import Item, Price
from django.db.models import Subquery, OuterRef, F, DecimalField, Func, Value, ExpressionWrapper, Max
from utils import timer

class HomeView(TemplateView):
    template_name = 'App/home/home.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.title = 'Home'
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    @timer
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
        # get the max 'date' for each item_id
        latest_dates = Price.objects.filter(
            item_id=OuterRef('item_id')
        ).values(
            'item_id'
        ).annotate(
            max_date=Max('date')
        ).values('max_date')[:1]

        # get 'price_new' for each item where 'date' = 'max_date' from latest_dates query
        latest_prices = Price.objects.filter(
            date=Subquery(latest_dates), item_id=OuterRef('item_id')
        ).values(
            'price_new'
        )[:1]

        percentage_change = (F('price_new') - Subquery(latest_prices)) / F('price_new') * -100

        order_by_expression = Func(
            F('price_change'),
            function='ABS',
            output_field=DecimalField()
        )

        result = Price.objects.filter(date='2023-11-10', price_new__gt=0).values(
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
        ).order_by(order_by_expression.desc())[:10]
        return result