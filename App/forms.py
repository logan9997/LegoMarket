from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.utils import ErrorList
from config import ModelsConfig, Input, METRICS
from .models import User
from django.http import HttpRequest, QueryDict
from decimal import Decimal
from django.db.models import Min, Max
from django.shortcuts import redirect
from utils import get_year_released_limit

class chartMetricSelect(forms.Form):
    choices = (
        (metric, ' '.join(word.capitalize() for word in metric.split('_'))) 
        for metric in METRICS
    )
    chart_metric = forms.ChoiceField(
        choices=choices,
        widget=forms.RadioSelect(attrs={
            'oninput': 'submit()',
            'class': 'metric-select-input'
        }),
        label=''
    )


class Login(forms.Form):
    username = forms.CharField(
        max_length=ModelsConfig.Length.USERNAME
    )
    password = forms.CharField(
        max_length=ModelsConfig.Length.PASSWORD, 
        widget=forms.PasswordInput()
    )

    def is_valid(self) -> bool:
        username = self.data.get('username')
        password = self.data.get('password')
        self.user = User.objects.filter(username=username, password=password)
        if self.user.exists():
            return True
        return False
    
    def get_user_id(self) -> int:
        return self.user.get().user_id


class SignUp(forms.Form):
    username = forms.CharField(
        max_length=ModelsConfig.Length.USERNAME
    )
    password = forms.CharField(
        max_length=ModelsConfig.Length.PASSWORD,
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        max_length=ModelsConfig.Length.PASSWORD,
        widget=forms.PasswordInput()
    )

    def is_valid(self) -> bool:
        username = self.data.get('username')
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')

        username_taken = User.objects.filter(username=username).exists()
        if password == confirm_password and not username_taken:
            return True
        return False
    

class SearchItem(forms.Form):
    q = forms.CharField(
        label='',
        error_messages={'required': ''},
        max_length=ModelsConfig.Length.ITEM_NAME,
        widget= forms.TextInput(attrs={
            'oninput': 'search_suggestions.show_search_suggestions()',
            'placeholder': 'Item Name / ID',
            'class': 'form-control mr-sm-2',
        }),
    )
    
    
class YearReleased(forms.Form):
    form_name = forms.CharField(
        widget=forms.HiddenInput(attrs={'value': 'year_released'}), 
        required=False
    )
    year_released = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'type': 'range',
                'min': get_year_released_limit(Min), 
                'max': get_year_released_limit(Max)
            }
        ),
    )


