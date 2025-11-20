from django.db import models
from decimal import Decimal

CURRENCY_CHOICES = [
    ('usd', 'USD'),
    ('eur', 'EUR'),
]


class Item(models.Model):
    """
    Модель товара.

    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def __str__(self):
        """
        Возвращает читабельное название товара.
        """
        return f"{self.name} ({self.currency.upper()} {self.price})"


class Order(models.Model):
    """
    Модель заказа.

    """
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, through='OrderItem')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def total_amount(self):
        """
        Возвращает итоговую стоимость заказа (сумма по каждому товару × количество).

        """
        total = Decimal('0')
        for oi in self.orderitem_set.all():
            total += oi.item.price * oi.quantity
        return total

    def __str__(self):
        """
        Текстовое отображение заказа в админке.
        """
        return f"Order #{self.id} ({self.currency.upper()})"


class OrderItem(models.Model):
    """
    Промежуточная модель для связи Order и Item.

    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """
        Удобное отображение товара внутри заказа.
        """
        return f"{self.item.name} × {self.quantity}"


class Discount(models.Model):
    """
    Модель скидки.

    """
    code = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 help_text="Уменьшение стоимости в валюте заказа")
    active = models.BooleanField(default=True)

    def __str__(self):
        """
        Отображение скидки в интерфейсе.
        """
        return f"{self.code} - {self.amount}"


class Tax(models.Model):
    """
    Модель налога.

    """
    name = models.CharField(max_length=100)
    percent = models.DecimalField(max_digits=5, decimal_places=2,
                                  help_text="Процент, применяемый к стоимости заказа")
    active = models.BooleanField(default=True)

    def __str__(self):
        """
        Удобное отображение налога.
        """
        return f"{self.name} ({self.percent}%)"
