from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import FormView
from typing import Any
from ..forms import Login, SignUp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants 
from utils import get_signup_error, AuthenticatedUserNotAllowed


def logout_view(request):
    logout(request)
    return redirect('home')


class LoginView(AuthenticatedUserNotAllowed, FormView):
    template_name = 'App/login/login.html'
    success_url = '/'
    form_class = Login
            
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'form': Login
        })
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        return super().post(request, *args, **kwargs)


class SignUpView(AuthenticatedUserNotAllowed, FormView):
    template_name = 'App/signup/signup.html'
    success_url = '/'
    form_class = SignUp

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        messages.add_message(request, constants.ERROR, 'Error Signing up')        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'form': SignUp
        })
        return context
            
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.add_message(request, constants.ERROR, 'Passwords do not match')
            return super().post(request, *args, **kwargs)

        try:
            user = User.objects.create_user(username, email, password)
            login(request, user)
            return redirect('home')
        except Exception as Error:
            error_message = get_signup_error(str(Error))
            messages.add_message(request, constants.ERROR, error_message)
            
        return super().post(request, *args, **kwargs)
    