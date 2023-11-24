from django import forms
from django.shortcuts import redirect
from config import METRICS, ModelsConfig, Input
from .models import User
from copy import copy

class chartMetricSelect(forms.Form):
    choices = (
        (metric, ' '.join(word.capitalize() for word in metric.split('_'))) 
        for metric in METRICS
    )
    metric_select = forms.ChoiceField(
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
    min_qty_used = forms.DecimalField(required=False)    
    max_qty_used = forms.DecimalField(required=False)    
    min_qty_new = forms.DecimalField(required=False)    
    max_qty_new = forms.DecimalField(required=False)    
    
    min_price_used = forms.DecimalField(required=False)    
    max_price_used = forms.DecimalField(required=False)    
    min_price_new = forms.DecimalField(required=False)    
    max_price_new = forms.DecimalField(required=False)    



class Pages(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Pages, self).__init__(*args, **kwargs)

        for button in Input.PAGE_BUTTON_INPUTS: 
            self.fields[button['name']] = forms.CharField(
                label='',
                widget=forms.TextInput(attrs={
                    'type': 'button',
                    'value':button['value'],
                    'onclick': 'submit()',
                })
            )
