from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from django.conf import settings
from .stripe_utils import create_checkout_session

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('product_list')

@login_required
def cart(request):
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    return render(request, 'shop/cart.html', {'order': order})

@login_required
def checkout(request):
    order = Order.objects.get(user=request.user, is_completed=False)
    session_id = create_checkout_session(order)
    context = {
        'order': order,
        'session_id': session_id,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'shop/checkout.html', context)
