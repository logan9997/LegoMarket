from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.utils import ErrorList
from config import ModelsConfig, Input, METRICS
from .models import User
from django.http import HttpRequest
from decimal import Decimal
from django.db.models import Min, Max
from utils import get_year_releaed

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
        max_length=ModelsConfig.Length.ITEM_NAME,
        widget= forms.TextInput(attrs={
            'oninput': 'search_suggestions.show_search_suggestions()',
            'placeholder': 'Item Name / ID',
            'class': 'form-control mr-sm-2',
        }),
    )
    
    
class MetricLimits(forms.Form):
    form_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    def __init__(self, *args, **kwargs):
        self.request:HttpRequest = kwargs.pop('request')
        super(MetricLimits, self).__init__(*args, **kwargs)
        self.set_fields()
        self.set_initial()

    def set_fields(self):
        for metric in METRICS:
            for limit in ['min', 'max']:
                field_name = f'{limit}_{metric}'
                self.fields[field_name] = forms.DecimalField(required=False, min_value=0)    

    def set_initial(self):
        self.initial = {
            field: self.request.GET.get(field, Decimal('0')) for field in self.fields
        }
        self.initial['form_name'] = 'metric_limits'



class ItemType(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ItemType, self).__init__(*args, **kwargs)
        self.set_initial()

    form_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    item_type = forms.ChoiceField(
        choices=(('M', 'Minifigure'), ('S', 'Set')),
        widget=forms.RadioSelect(attrs={'onclick': 'submit()'})
    )

    def set_initial(self):
        self.initial['form_name'] = 'item_type'


class YearReleased(forms.Form):

    def __init__(self, *args, **kwargs):
        super(YearReleased, self).__init__(*args, **kwargs)
        self.set_initial()

    form_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    year_released = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'type': 'range',
            'min': get_year_releaed(Min),
            'max':get_year_releaed(Max),
        })
    )

    def set_initial(self):
        self.initial['form_name'] = 'year_released'