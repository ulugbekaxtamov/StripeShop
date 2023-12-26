from django.views import generic
from django.shortcuts import redirect

from main.settings import STRIPE_PUBLIC_TOKEN
from .manager import CartSession
from .models import Item, Tax, Discount, Order


def root(request):
    return redirect('product:item_list')  # Редирект на product_list


class ItemListView(generic.ListView):
    template_name = 'product_list.html'
    queryset = Item.objects.all()
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        cart_session = CartSession(self.request)
        context['stripe_public_key'] = STRIPE_PUBLIC_TOKEN
        context['cart_count'] = cart_session.__len__()
        context['cart_list'] = cart_session.cart
        return context


class ItemDetailView(generic.DetailView):
    template_name = 'product_detail.html'
    queryset = Item.objects.all()
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        cart_session = CartSession(self.request)
        context['stripe_public_key'] = STRIPE_PUBLIC_TOKEN
        context['cart_count'] = cart_session.__len__()
        context['cart_list'] = cart_session.cart
        return context


class CartListView(generic.TemplateView):
    template_name = 'cart_list.html'

    def get_context_data(self, **kwargs):
        context = super(CartListView, self).get_context_data(**kwargs)
        currency = self.request.GET.get('currency') if 'currency' in self.request.GET else "usd"
        self.request.session['currency'] = currency

        cart_session = CartSession(self.request)
        context['item_list'] = cart_session.get_cart_items()
        context['cart_count'] = cart_session.__len__()

        context['data'] = cart_session.get_total_amount(currency)
        context['currency'] = currency.upper()
        return context


class OrderListView(generic.ListView):
    template_name = 'order_list.html'
    queryset = Order.objects.all()
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        cart_session = CartSession(self.request)
        context['cart_count'] = cart_session.__len__()
        return context


class OrderPayView(generic.DetailView):
    template_name = 'order_pay.html'
    queryset = Order.objects.all()
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderPayView, self).get_context_data(**kwargs)

        cart_session = CartSession(self.request)
        context['cart_count'] = cart_session.__len__()

        context['stripe_public_key'] = STRIPE_PUBLIC_TOKEN
        return context
