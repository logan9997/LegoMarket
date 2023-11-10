from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import FormView
from typing import Any
from ..forms import Login


class LoginView(FormView):
    template_name = 'App/login/login.html'
    success_url = '/'
    form_class = Login
            
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = Login(request.POST)
        if form.is_valid():
            user_id = form.get_user_id()
            request.session['user_id'] = user_id
            return redirect('home')
        return super().post(request, *args, **kwargs)
    
    