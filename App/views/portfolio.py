from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView
from ..models import Portfolio
from ..forms import PortfolioItem, chartMetricSelect
from typing import Any
from utils import get_previous_url, Chart, get_portfolio_item_inventory
from django.db.models import Subquery, OuterRef, Count, F
import json
from django.contrib.auth.mixins import LoginRequiredMixin


def update_portfolio_item(request: HttpRequest, entry_id: int, item_id: str):

    # if not request.user.is_authenticated:
    #     return redirect(get_previous_url(request))

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
            previous_url += f'#modal_{item_id}'         

    return redirect(previous_url)


def delete_portfolio_item(request: HttpRequest, entry_id: int, item_id: str):
    previous_url = get_previous_url(request)

    if request.method == 'POST':
        delete_item = Portfolio.objects.get(entry_id=entry_id)

        user_id = request.user.id
        if delete_item.user.pk != user_id:
            return redirect(previous_url)

        delete_item.delete()
        previous_url += f'#modal_{item_id}'
    return redirect(previous_url)


def add_portfolio_item(request: HttpRequest, item_id: str):
    user_id = request.user.id
    previous_url = get_previous_url(request)
    if user_id == -1:
        return redirect(previous_url)
    print('previous_url-', previous_url)

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
            previous_url += f'#modal_{item_id}'

    print('previous_url-', previous_url)
    return redirect(previous_url)

class PortfolioView(LoginRequiredMixin, TemplateView):
    template_name = 'App/portfolio/portfolio.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.user_id = request.user.id
        self.portfolio_item_ids = self.get_portfolio_item_ids()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.portfolio_item_ids: 
            context.update({
                'portfolio_items': list(self.get_portfolio_items()),
                'inventories': self.get_inventories(),
                'charts': self.get_chart_datasets(),
                'chart': self.get_chart_data_dict(self.get_portfolio_item_ids()[0], jsonify=False),
                'forms': {
                    'chart_metric_select': chartMetricSelect,
                    'portfolio_item': PortfolioItem
                }
            })
        return context
    
    def get_inventories(self):
        inventories = {}
        for item_id in self.portfolio_item_ids:
            inventories[item_id] = get_portfolio_item_inventory(item_id, self.user_id)
        return inventories

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
    
    def get_chart_data_dict(self, item_id: str, jsonify=True) -> dict[str, Any]:
        self.chart = Chart(self.request, item_id)
        metric = self.chart.get_selected_chart_metric()
        chart_data = self.chart.get_chart_data(metric)
        data = {
            'data': chart_data,
            'labels': self.chart.get_chart_data('date'),
            'metric': self.chart.get_selected_chart_metric(),
            'metric_difference': chart_data[-1]  - chart_data[0],
            'metric_percentage_difference': self.chart.get_metric_percentage_change(metric)
        }

        if jsonify:
            data['data'] = json.dumps(data['data'], default=str)
            data['labels'] = json.dumps(data['labels'], default=str)

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