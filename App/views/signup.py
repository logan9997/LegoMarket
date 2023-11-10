from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import FormView
from typing import Any
from ..forms import SignUp
from ..models import User


class SignUpView(FormView):
    template_name = 'App/signup/signup.html'
    success_url = '/'
    form_class = SignUp
            
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = SignUp(request.POST)
        if form.is_valid():
            username = form.data.get('username')
            password = form.data.get('password')

            new_user = User.objects.create(
                username=username,
                password=password
            )
            new_user.save()
            request.session['user_id'] = new_user.user_id
        return super().post(request, *args, **kwargs)
    
    

