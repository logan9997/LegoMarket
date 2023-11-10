from django.urls import path
from .views import (
    home, item, login
)

urlpatterns = [
    path('', home.home, name='home'),
    path('item/<str:item_id>/', item.ItemView.as_view(), name='item'),
    path('login/', login.LoginView.as_view(), name='login')
]