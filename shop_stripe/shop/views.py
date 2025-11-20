import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from .models import Item, Order
from django.views.decorators.http import require_GET, require_POST

from django.http import HttpResponse

def index(request):
    return HttpResponse("Привет, Stripe магазин!")


def _select_stripe_keys_for_currency(currency):
    """
    Если нужно использовать разные keypairs для валют — выбираем нужные ключи.
    """
    if currency.lower() == 'eur' and getattr(settings, 'STRIPE_SECRET_KEY_EUR', None):
        return settings.STRIPE_SECRET_KEY_EUR, settings.STRIPE_PUBLISHABLE_KEY_EUR
    return settings.STRIPE_SECRET_KEY, settings.STRIPE_PUBLISHABLE_KEY

@require_GET
def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    # передаём publishable key в шаблон
    _, publishable = _select_stripe_keys_for_currency(item.currency)
    return render(request, 'shop/item_detail.html', {
        'item': item,
        'stripe_publishable_key': publishable
    })

@require_GET
def buy_item(request, id):
    item = get_object_or_404(Item, id=id)
    secret_key, _ = _select_stripe_keys_for_currency(item.currency)
    stripe.api_key = secret_key

    # Stripe expects amount in cents (integer)
    unit_amount = int(item.price * Decimal('100'))

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'description': item.description[:300],
                },
                'unit_amount': unit_amount,
            },
            'quantity': 1,
        }],
        success_url=settings.SUCCESS_URL + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=settings.CANCEL_URL,
    )
    return JsonResponse({'id': session.id})

# Альтернативный эндпоинт — PaymentIntent (возвращает client_secret)
@require_POST
def create_payment_intent(request, id):
    item = get_object_or_404(Item, id=id)
    secret_key, _ = _select_stripe_keys_for_currency(item.currency)
    stripe.api_key = secret_key

    amount = int(item.price * Decimal('100'))
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=item.currency,
        payment_method_types=['card'],
        metadata={'item_id': item.id}
    )
    return JsonResponse({'client_secret': intent.client_secret})

