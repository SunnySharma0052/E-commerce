from django.shortcuts import render
from .models import Category, Product
from cart.models import Cart, Wishlist  # Assuming you have a cart app with CartItem model



# Create your views here.
# core/views.py

def home(request):
    # Featured categories
    featured_categories = Category.objects.filter(
        is_featured_categories=True,
        products__is_available=True
    ).distinct()[:8]

    # Products
    popular_products = Product.objects.filter(is_popular=True, is_available=True)
    daily_best_sells = Product.objects.filter(is_daily_best_sell=True, is_available=True)

    # Ensure session exists
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    # Get cart items using session_key
    cart_items = Cart.objects.filter(session_key=session_key)
    total_cart_quantity = sum(item.quantity for item in cart_items)

    # Get wishlist items count using session_key
    wishlist_items = Wishlist.objects.filter(session_key=session_key)
    wishlist_count = wishlist_items.count()

    context = {
        'featured_categories': featured_categories,
        'popular_products': popular_products,
        'daily_best_sells': daily_best_sells,
        'cart_item_count': total_cart_quantity,
        'wishlist_count': wishlist_count,      # <-- add wishlist count here
    }

    return render(request, 'core/home.html', context)
