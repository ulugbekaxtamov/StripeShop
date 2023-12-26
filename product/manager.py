from product.models import Item, Discount, Tax


class CartSession:
    """
        CartSession manages a shopping cart session for a user.
        It handles adding, removing items, and calculating totals in the cart.
    """

    def __init__(self, request):
        self.session = request.session
        cart_session = self.session.get('cart')
        if 'cart' not in self.session or not cart_session:
            cart_session = self.session['cart'] = []
        self.cart = cart_session

    def add_item(self, item_id: int):
        if item_id not in self.cart:
            self.cart.append(item_id)
            self.save()

    def remove_item(self, item_id: int):
        if item_id in self.cart:
            self.cart.remove(item_id)
            self.save()

    def clear(self):
        self.session['cart'] = []

    def save(self):
        self.session.modified = True

    def get_cart_items(self):
        item_ids = self.cart
        return Item.objects.filter(id__in=item_ids)

    def get_total_price_items(self, target_currency="usd"):
        """
            Calculates the total price of items in the cart.
            Sums the prices of all items in the cart, converting them to the target currency.
        """

        total = 0

        for item_id in self.cart:
            item = Item.objects.get(id=item_id)
            total += item.get_price(target_currency)

        return round(total, 2)

    def get_total_amount(self, target_currency="usd"):
        """
            Calculates the total amount for the cart.
            Includes the effects of the latest tax and any applicable discount.
            Returns a dictionary with the total amount, total price of items, tax, and discount.
        """

        tax = Tax.objects.last()
        tax = tax.percentage if tax else 0

        discount = Discount.objects.filter(more_than_items__lte=self.__len__()).first()
        discount = discount.percentage if discount else 0

        total_price_items = self.get_total_price_items(target_currency=target_currency)
        tax_amount = tax * total_price_items / 100

        discount_amount = discount * total_price_items / 100
        total_amount = tax_amount - discount_amount + total_price_items

        return {'total_amount': round(total_amount, 2), 'total_price_items': total_price_items, 'tax': tax,
                'discount': discount}

    def __len__(self):
        return len(self.cart)
