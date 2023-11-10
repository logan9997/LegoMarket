from django import forms
from config import METRICS, ModelsConfig
from .models import User

class GraphMetricSelect(forms.Form):
    metric_select = forms.ChoiceField(choices=(
        (metric, ' '.join(word.capitalize() for word in metric.split('_'))) for metric in METRICS)
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
    
    def get_user_id(self):
        return self.user.get().user_id
