from django.urls import path
from .views import (
    home, item
)

urlpatterns = [
    path('', home.home, name='home'),
    path('item/<str:item_id>/', item.ItemView.as_view(), name='item')
]