from django import forms
from config import METRICS, ModelsConfig
from .models import User

class chartMetricSelect(forms.Form):
    metric_select = forms.ChoiceField(
        choices=(
            (metric, ' '.join(word.capitalize() for word in metric.split('_'))) for metric in METRICS
        ),
        widget=forms.Select(attrs={'oninput': 'this.form.submit()'})
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
    search_value = forms.CharField(
        label='',
        max_length=ModelsConfig.Length.ITEM_NAME,
        widget= forms.TextInput(attrs={
            'oninput': 'new SearchSuggestions().show_search_suggestions()',
            'placeholder': 'Item Name / ID',
            'class': 'form-control mr-sm-2'
        }),
    )