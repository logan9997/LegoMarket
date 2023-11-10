from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponse
from django.views.generic import FormView
from typing import Any
from ..forms import Login


class LoginView(FormView):
    template_name = 'App/login/login.html'
    success_url = '/'
    form_class = Login
            
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.request = request
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form: Any) -> HttpResponse:
        user_id = form.get_user_id()
        self.request.session['user_id'] = user_id
        return super().form_valid(form)
    