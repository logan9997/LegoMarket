from django.urls import path
from .views import (
    home, item, authenticate, search, portfolio
)

urlpatterns = [
    path('', home.HomeView.as_view(), name='home'),
    path('search/', search.SearchView.as_view(), name='search'),
    path('search_form_hander/', search.FormHandler.as_view(), name='search_form_hander'),
    path('item/<str:item_id>/', item.ItemView.as_view(), name='item'),
    path('portfolio/', portfolio.PortfolioView.as_view(), name='portfolio'),
    path('portfolio_item/<str:item_id>', portfolio.PortfolioItemView.as_view(), name='portfolio_item'),
    path('add_portfolio_item/<str:item_id>/', portfolio.add_portfolio_item, name='add_portfolio_item'),
    path('delete_portfolio_item/<int:entry_id>/<str:item_id>', portfolio.delete_portfolio_item, name='delete_portfolio_item'),
    path('update_portfolio_item/<int:entry_id>/<str:item_id>', portfolio.update_portfolio_item, name='update_portfolio_item'),   
    path('login/', authenticate.LoginView.as_view(), name='login'),
    path('signup/', authenticate.SignUpView.as_view(), name='signup'),
    path('logout/', authenticate.logout_view, name='logout')
]