from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView
from ..models import Item, Price, Portfolio
from ..forms import PortfolioItem
from typing import Any
from decimal import Decimal
from utils import get_user_id, get_previous_url

def delete_portfolio_item(request: HttpRequest, entry_id: int):
    if request.method == 'POST':
        delete_item = Portfolio.objects.filter(entry_id=entry_id)
        delete_item.delete()
    previous_url = get_previous_url(request)
    return redirect(f'{previous_url}#openModal')

def add_to_portfolio(request: HttpRequest, item_id: str):
    if request.method == 'POST':
        form = PortfolioItem(request.POST)
        if form.is_valid():
            data: dict = form.cleaned_data
            new_portfolio_item = Portfolio(
                user_id=get_user_id(request),
                item_id=item_id,
                **data
            )
            new_portfolio_item.save()

    previous_url = get_previous_url(request)
    return redirect(f'{previous_url}#openModal')


class PortfolioView(TemplateView):
    template_name = 'App/portfolio/portfolio.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.user_id = request.session.get('user_id', -1)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'portfolio_items': self.get_portfolio_items()
        })
        return context
    
    def get_portfolio_items(self):
        '''
        Return items from Portfolio model where item_id = self.item_id
        '''
        print('a')
        items = Portfolio.objects.filter(user_id=self.user_id)
        for item in items:
            for k, v in item.items():
                print(k, v)
        return items