from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView
from ..models import Item, Price, Portfolio
from ..forms import PortfolioItem
from typing import Any
from decimal import Decimal
from utils import get_user_id, get_previous_url, get_portfolio_item_inventory, Chart
from django.db.models import Subquery, OuterRef, Count, F

def update_portfolio_item(request: HttpRequest, entry_id: int):
    previous_url = get_previous_url(request)
    if request.method == 'POST':
        form = PortfolioItem(request.POST)
        if form.is_valid():
            update_item = Portfolio.objects.get(entry_id=entry_id)
            for k, v in form.cleaned_data.items():
                if v == None and getattr(update_item, k) != None:
                    setattr(update_item, k, v)
                if v != None:
                    setattr(update_item, k, v)

            update_item.save()

    if previous_url != 'home':
        previous_url += '#openModal'         
    return redirect(previous_url)


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


def add_portfolio_item(request: HttpRequest, item_id: str):
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
            'portfolio_items': self.get_portfolio_items(),
            'charts': self.get_chart_datasets()
        })
        return context
    
    def get_portfolio_items(self):
        '''
        Return items from Portfolio model where item_id = self.item_id
        '''
        items = (
            Portfolio.objects.filter(
                user_id=self.user_id
            ).values(
                'item_id',
                image_path=F('item__image_path'),
                item_name=F('item__item_name'),
            ).annotate(
                count=Subquery(
                    Portfolio.objects.filter(
                        user_id=OuterRef('user_id'),
                        item_id=OuterRef('item_id')
                    ).values(
                        'item_id'
                    ).annotate(
                        count=Count('item_id')
                    ).values(
                        'count'
                    )[:1]
                )
            ).distinct()
        )
        return items
    
    def get_portfolio_item_ids(self):
        item_ids = Portfolio.objects.filter(
            user_id=self.user_id
        ).distinct().values_list(
            'item_id', flat=True
        )
        return item_ids
    
    def get_chart_data_dict(self, item_id: str) -> dict[str, Any]:
        self.chart = Chart(self.request, item_id)
        selected_chart_metric = self.chart.get_selected_chart_metric()
        data = {
            'chart_metrics': self.chart.get_chart_data(selected_chart_metric),
            'chart_dates': self.chart.get_chart_data('date'),
            'chart_id': self.chart.get_chart_id()
        }
        return data
    
    def get_chart_datasets(self) -> list[dict[str, Any]]:
        item_ids = self.get_portfolio_item_ids()
        datasets = []
        for item_id in item_ids:
            datasets.append(self.get_chart_data_dict(item_id))
        return datasets

class PortfolioItemView(TemplateView):
    template_name = 'App/portfolio/portfolio_item.html'
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({

        })
        return context