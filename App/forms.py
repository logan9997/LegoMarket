from django import forms
from config import ModelsConfig, METRICS, DATE_FORMAT
from .models import User
from django.http import HttpRequest
from django.db.models import Min, Max
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

    def __init__(self, request: HttpRequest, *args, **kwargs):
        super(SearchItem, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['q'].initial = self.request.GET.get('q', '')

    q = forms.CharField(
        label='',
        required=False,
        max_length=ModelsConfig.Length.ITEM_NAME,
        widget= forms.TextInput(attrs={
            'oninput': 'search_suggestions.show_search_suggestions()',
            'placeholder': 'Item Name / ID',
            'class': 'form-control mr-sm-2',
        }),
    )
    

class DivWrapper(forms.CheckboxInput):
    def render(self, name, value, attrs=None, renderer=None):
        input = super().render(name, value, attrs)
        html = f'''
            <div class="checkbox-wrapper">
                {input}
                <label>{name.capitalize()}</label>
            </div>
        '''
        return html


class ClearableForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ClearableForm, self).__init__(*args, **kwargs)
        self.set_clear_index()

    def set_clear_index(self) -> None:
        fields = list(self.fields.items())
        clear_button = fields.pop(0)
        fields.append(clear_button)
        self.fields = dict(fields)

    clear = forms.BooleanField(
        required=False,
        label='',
        widget=DivWrapper(
            attrs={
                'onclick': 'submit()',
                'class': 'clear-button',
            }
        )
    )


class Order(forms.Form):
    form_name = forms.CharField(
        widget=forms.HiddenInput(attrs={'value': 'order'}), 
        required=False
    )
    order = forms.ChoiceField(
        widget=forms.Select(attrs={'oninput': 'submit()'}),
        label='Sort By:',
        choices=(
            ('item_id', 'Item ID Asc'),
            ('-item_id', 'Item ID Desc'),
            ('item_name', 'Item Name Asc'),
            ('-item_name', 'Item Name Desc'),
            ('-year_released', 'Newest Release'),
            ('year_released', 'Oldest Release'),
            ('-price_new', 'Highest Price (New)'),
            ('price_new', 'Lowest Price (New)'),
            ('-price_used', 'Highest Price (Used)'),
            ('price_used', 'Lowest Price (Used)'),
            ('-qty_new', 'Highest Qty (New)'),
            ('qty_new', 'Lowest Qty (New)'),
            ('-qty_used', 'Highest Qty (Used)'),
            ('qty_used', 'Lowest Qty (Used)'),
        ), 
    )

    def set_initial(request):
        return {'order': request.GET.get('order')}


class YearReleased(ClearableForm):
    form_name = forms.CharField(
        widget=forms.HiddenInput(attrs={'value': 'year_released'}), 
        required=False
    )

    year_released = forms.IntegerField(
        label='',
        widget=forms.TextInput(
            attrs={
                'type': 'range',
                'min': get_year_released_limit(Min), 
                'max': get_year_released_limit(Max),
                'onchange': 'submit()'
            }
        ),
    )

    def set_initial(request):
        return {'year_released': request.GET.get('year_released')}


class ItemType(forms.Form):
    form_name = forms.CharField(
        widget=forms.HiddenInput(attrs={'value': 'item_type'}), 
        required=False
    )

    item_type = forms.ChoiceField(
        choices=(('M', 'Minifigure'), ('S', 'Set'), ('All', 'All')),
        widget=forms.RadioSelect(attrs={'onclick': 'submit()'}),
        label=''
    )

    def set_initial(request):
        return {'item_type': request.GET.get('item_type', 'All')}


class MetricLimits(ClearableForm):
    form_name = forms.CharField(
        widget=forms.HiddenInput(attrs={'value': 'metric_limits'}), 
        required=False,
        label=''
    )

    kwargs = {'min_value':0, 'required':False, 'initial':0}
    min_price_new = forms.DecimalField(**kwargs, label='Min Price (New) (£)')
    max_price_new = forms.DecimalField(**kwargs, label='Max Price (New) (£)')
    min_price_used = forms.DecimalField(**kwargs, label='Min Price (Used) (£)')
    max_price_used = forms.DecimalField(**kwargs, label='Max Price (Used) (£)')
    min_qty_new = forms.IntegerField(**kwargs, label='Min Qty (New)')
    max_qty_new = forms.IntegerField(**kwargs, label='Max Qty (New)')
    min_qty_used = forms.IntegerField(**kwargs, label='Min Qty (Used)')
    max_qty_used = forms.IntegerField(**kwargs, label='Max Qty (Used)')

    def set_initial(request):
        initial = {
            'min_price_new': request.GET.get('min_price_new', 0),
            'max_price_new': request.GET.get('max_price_new', 0),
            'min_price_used': request.GET.get('min_price_used', 0),
            'max_price_used': request.GET.get('max_price_used', 0),
            'min_qty_new': request.GET.get('min_qty_new', 0),
            'max_qty_new': request.GET.get('max_qty_new', 0),
            'min_qty_used': request.GET.get('min_qty_used', 0),
            'max_qty_used': request.GET.get('max_qty_used', 0),
        }
        return initial


class PortfolioItem(forms.Form):
    bought_for = forms.DecimalField(
        required=False
    )
    date_acquired = forms.DateField(
        required=False,
        input_formats=[DATE_FORMAT],
        widget=forms.DateInput(
            attrs={
                'pattern':'\d{4}-\d{2}-\d{2}',
                'placeholder': 'YYYY-MM-DD  '
            }
        )
    )
    notes = forms.CharField(
        max_length=ModelsConfig.Length.NOTES,
        required=False
    )