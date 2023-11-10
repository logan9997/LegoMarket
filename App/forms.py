from django import forms
from config import METRICS

class GraphMetricSelect(forms.Form):
    metric_select = forms.ChoiceField(choices=(
        (metric, ' '.join(word.capitalize() for word in metric.split('_'))) for metric in METRICS)
    )