from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import TemplateView
from typing import Any

class HoHomeViewme(TemplateView):
    template_name = 'App/home/home.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
        })
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

