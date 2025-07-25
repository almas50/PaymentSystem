from django.urls import path
from . import views

urlpatterns = [
    path('api/buy/<int:pk>/', views.BuyItemApiView.as_view(), name='buy-item'),
    path('item/<int:pk>/', views.item_page_view, name='item_page'),
    path("api/buy-order/<int:pk>/", views.BuyOrderApiView.as_view(), name="buy_order_api"),
    path('order/<int:pk>/', views.order_page_view, name='order_page'),
]