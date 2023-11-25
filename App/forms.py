from django import forms
from config import ModelsConfig, Input
from .models import User

class chartMetricSelect(forms.Form):
    choices = (
        (metric, ' '.join(word.capitalize() for word in metric.split('_'))) 
        for metric in Input.METRICS
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
    def __init__(self, *args, **kwargs):
        super(MetricLimits, self).__init__(*args, **kwargs)
        for metric in Input.METRICS:
            for limit in ['min', 'max']:
                field_name = f'{limit}_{metric}'
                self.fields[field_name] = forms.DecimalField(required=False)    
       

