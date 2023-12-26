from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect

from main import settings
from product.models import Item, Order, Tax, Discount
from product.manager import CartSession
from . import serializers
import stripe


# Cart
class CartAddItemAPIView(APIView):
    """
       API view for adding an item to the cart. Returns a 201 Created status on success,
       and a 404 Not Found status if the item does not exist.
    """

    def post(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            cart = CartSession(request)
            cart.add_item(item_id)
            return Response({"message": "Item added to cart successfully."}, status=status.HTTP_202_ACCEPTED)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


class CartRemoveItemAPIView(APIView):
    """
        API view for removing an item from the cart.
        Returns a 204 No Content status on successful removal.
    """

    def delete(self, request, item_id):
        cart = CartSession(request)
        cart.remove_item(item_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartClearAPIView(APIView):
    """
        API view for clearing the cart's contents.
        Returns a 200 OK status with data of the cleared cart.
    """

    def post(self, request):
        cart = CartSession(request)
        cart.clear()
        serializer = serializers.CartSessionSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class OrderRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
        API view for retrieving and updating an order.
        Returns a 200 OK status by default.
    """

    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    lookup_field = 'id'


class BuyItemAPIView(APIView):
    """
        API view for creating a payment session for an item via Stripe.
        Returns a 200 OK status upon successful session creation.
    """

    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        tax = Tax.objects.last()
        tax_rate_id = tax.tax_id if tax else None

        stripe.api_key = settings.STRIPE_SECRET_TOKEN
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
                'tax_rates': [tax_rate_id] if tax_rate_id else [],
            }],
            # discounts=[{"coupon": "3R8lSDNG"}],
            mode='payment',
            success_url=request.build_absolute_uri('/') + '?success=true',
            cancel_url=request.build_absolute_uri('/') + '?canceled=true',
        )
        return Response({'session_id': session.id, 'redirect_url': session.url}, status=status.HTTP_200_OK)


class PaymentOrderAPIView(APIView):
    """
        API view for processing an order and creating a Stripe payment intent.
        Returns a 201 Created status on successful order creation.
    """

    def post(self, request):
        cart = CartSession(request)
        currency = self.request.session.get('currency')

        tax = Tax.objects.last()
        discount = Discount.objects.filter(more_than_items__lte=cart.__len__()).first()

        order = Order.objects.create(
            currency=currency if currency else "usd",
            tax=tax,
            discount=discount
        )

        item_ids = cart.get_cart_items()
        items = Item.objects.filter(id__in=item_ids)
        order.items.add(*items)

        total_price = int(cart.get_total_amount(currency)['total_amount'] * 100)
        stripe.api_key = settings.STRIPE_SECRET_TOKEN
        payment_intent = stripe.PaymentIntent.create(
            description=f'Order ID {order.id}',
            amount=total_price,
            currency=currency,
            automatic_payment_methods={"enabled": True},
        )
        order.intent_id = payment_intent.id
        order.intent_client_secret = payment_intent.client_secret
        order.save()
        cart.clear()
        return Response({"order_id": order.id})
