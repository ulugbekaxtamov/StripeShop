from django.urls import path
from . import views

app_name = 'api_product'
urlpatterns = [

    # Cart
    path('cart/add/<int:item_id>/', views.CartAddItemAPIView.as_view(), name='cart-add-item'),
    path('cart/remove/<int:item_id>/', views.CartRemoveItemAPIView.as_view(),
         name='cart-remove-item'),
    path('cart/clear/', views.CartClearAPIView.as_view(), name='cart-clear'),

    path('order/<int:id>/', views.OrderRetrieveUpdateAPIView.as_view(), name='order-retrieve-update'),

    path('buy/item/<int:item_id>/', views.BuyItemAPIView.as_view(), name='buy-item'),
    path('payment/order/', views.PaymentOrderAPIView.as_view(), name='payment-order'),
]
