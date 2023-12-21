from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView
from ..models import Item, Price, Portfolio
from ..forms import PortfolioItem
from typing import Any
from decimal import Decimal
from utils import get_user_id, get_previous_url, get_portfolio_item_inventory


def delete_portfolio_item(request: HttpRequest, entry_id: int):
    previous_url = get_previous_url(request)

    if request.method == 'POST':
        delete_item = Portfolio.objects.get(entry_id=entry_id)

        user_id = get_user_id(request)
        if delete_item.user.user_id != user_id:
            return redirect(previous_url)

        delete_item.delete()

    if previous_url != 'home':
        previous_url += '#openModal'
    return redirect(previous_url)

def add_to_portfolio(request: HttpRequest, item_id: str):

    user_id = get_user_id(request)
    previous_url = get_previous_url(request)
    if user_id == -1:
        return redirect(previous_url)

    if request.method == 'POST':
        form = PortfolioItem(request.POST)
        if form.is_valid():
            data: dict = form.cleaned_data
            new_portfolio_item = Portfolio(
                user_id=user_id,
                item_id=item_id,
                **data,
            )
            new_portfolio_item.save()

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
        items = Portfolio.objects.filter(user_id=self.user_id)
