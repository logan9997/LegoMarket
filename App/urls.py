from django.urls import path
from .views import (
    home, item, login, signup, search, 
)

urlpatterns = [
    path('', home.home, name='home'),
    path('search/', search.SearchView.as_view(), name='search'),
    path('search_form_hander/', search.FormHandler.as_view(), name='search_form_hander'),
    path('item/<str:item_id>/', item.ItemView.as_view(), name='item'),
    path('login/', login.LoginView.as_view(), name='login'),
    path('signup/', signup.SignUpView.as_view(), name='signup'),
]