from django.urls import path, include
from product import views

app_name = 'product'
urlpatterns = [
    path('', views.root, name='root'),

    path('product/list/', views.ItemListView.as_view(), name='item_list'),
    path('product/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),

    path('cart/list/', views.CartListView.as_view(), name='cart_list'),
    path('order/list/', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/pay/', views.OrderPayView.as_view(), name='order_pay'),
]
