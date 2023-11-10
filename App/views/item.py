from django.http import HttpRequest
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from ..models import Item
from typing import Any

class ItemView(TemplateView):
    template_name = 'App/item/item.html'

    def dispatch(self, request:HttpRequest, item_id:str, *args, **kwargs) -> HttpResponse:
        self.item_id = item_id
        self.title = f'Item/{self.item_id}'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['item_info'] = self.get_item_info()
        return context
    
    def get_item_info(self):
        return Item.objects.get(item_id=self.item_id)
    
