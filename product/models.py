from django.db import models
from base.models import Base


class Item(Base):
    class Meta:
        ordering = ('-id',)

    CURRENCY_RATES = {"usd": 1.0, "eur": 0.85}

    CURRENCY_CHOICES = (
        ("usd", "USD"),
        ("eur", "EUR")
    )

    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    def get_price(self, target_currency: str = None):
        """
            Calculates the price of the item in a specified target currency.
            If no target currency is specified, or it matches the item's currency,
            returns the original price. Otherwise, performs a currency conversion.
            Handles unsupported currency conversion by raising a ValueError.
        """

        if not target_currency or target_currency == self.currency:
            return float(self.price)

        try:
            if self.currency in self.CURRENCY_RATES and target_currency in self.CURRENCY_RATES:
                item_price = float(self.price) * (
                        self.CURRENCY_RATES[target_currency] / self.CURRENCY_RATES[self.currency])
                return round(item_price, 2)
            else:
                raise ValueError("Unsupported currency conversion")
        except Exception as e:
            print(f"Error in currency conversion: {e}")
            return None

    def __str__(self):
        return f"{self.id} - {self.name}"


class Order(Base):
    class Meta:
        ordering = ('-id',)

    CURRENCY_CHOICES = (
        ("usd", "USD"),
        ("eur", "EUR")
    )

    items = models.ManyToManyField(Item)
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True)
    tax = models.ForeignKey('Tax', on_delete=models.SET_NULL, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    intent_id = models.CharField(max_length=255, null=True, blank=True)
    intent_client_secret = models.CharField(max_length=255, null=True, blank=True)

    is_paid = models.BooleanField(default=False)

    def get_total_item_price(self):
        """
            Calculates the total price of all items in the order, using the order's currency.
            This total is calculated before applying any discounts or taxes.
        """

        items_total_price = sum([item.get_price(target_currency=self.currency) for item in self.items.all()])
        return items_total_price

    def get_total_amount(self):
        """
            Calculates the final total amount of the order, including any discounts and taxes.
            First, it computes the total price of items, then applies the discount (if any),
            and finally adds tax to the discounted total.
        """

        total_amount = sum([item.get_price(target_currency=self.currency) for item in self.items.all()])

        if self.discount:
            discount_amount = self.discount.percentage * total_amount / 100
            total_amount -= discount_amount
        if self.tax:
            tax_amount = self.tax.percentage * total_amount / 100
            total_amount += tax_amount

        return round(total_amount, 2)


class Discount(Base):
    name = models.CharField(max_length=100)
    percentage = models.FloatField()
    more_than_items = models.IntegerField(default=3)
    discount_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Tax(Base):
    name = models.CharField(max_length=100)
    percentage = models.FloatField()
    tax_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name}"
