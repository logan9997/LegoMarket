from django.urls import path
from .views import (
    home, item, login, signup, search_form, search
)

urlpatterns = [
    path('', home.home, name='home'),
    path('search_form', search_form.search_form, name='search_form'),
    path('search/', search.SearchView.as_view(), name='search'),
    path('item/<str:item_id>/', item.ItemView.as_view(), name='item'),
    path('login/', login.LoginView.as_view(), name='login'),
    path('signup/', signup.SignUpView.as_view(), name='signup'),
]