import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(order):
    line_items = [{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': item.product.name,
            },
            'unit_amount': int(item.product.price * 100),
        },
        'quantity': item.quantity,
    } for item in order.orderitem_set.all()]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://localhost:8000/shop/success/',
        cancel_url='http://localhost:8000/shop/cancel/',
    )

    return session.id
