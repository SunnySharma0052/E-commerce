from django.shortcuts import render, redirect, get_object_or_404
from core.models import Product
from cart.models import Cart

# Create your views here.
# Home page (optional)
def cart_navbar(request):
    return render(request, 'core/home.html')







# Login error page
def cart_login_error(request):
    if 'user_id' in request.session:
        return redirect('view_cart')
    return render(request, 'cart/cart_login_error.html')








# View cart
def chunk_products(products, size):
    """Split products list into chunks of given size."""
    return [products[i:i + size] for i in range(0, len(products), size)]


# View cart
def view_cart(request):
    # Check for login via session
    if 'user_id' not in request.session:
        return redirect('cart_login_error')

    # Ensure session key exists
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # Fetch cart items associated with session
    cart_queryset = Cart.objects.filter(session_key=session_key)
    cart_items = []
    total = 0
    categories = set()

    for item in cart_queryset:
        subtotal = item.product.price * item.quantity
        total += subtotal
        cart_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': subtotal
        })
        categories.add(item.product.category)

    # Get recently viewed product IDs from session (most recent first)
    recently_viewed_ids = request.session.get('recently_viewed', [])
    recently_viewed_products = Product.objects.filter(id__in=recently_viewed_ids)
    
    # Preserve the order of recently_viewed_ids
    id_to_product = {product.id: product for product in recently_viewed_products}
    ordered_recently_viewed = [id_to_product[_id] for _id in recently_viewed_ids if _id in id_to_product]

    # Group into chunks of 5 for carousel
    recently_viewed_groups = chunk_products(ordered_recently_viewed[:18], 4)

    # Suggest similar products from the same categories, excluding items already in cart
    similar_products = Product.objects.filter(category__in=categories).exclude(
        id__in=[item['product'].id for item in cart_items]
    ).distinct()

    context = {
        'cart_items': cart_items,
        'total': total,
        'recently_viewed_groups': recently_viewed_groups,
        'similar_products': similar_products,
    }

    return render(request, 'cart/cart.html', context)

# Add to cart
def add_to_cart(request, product_id):
    if 'user_id' not in request.session:
        return redirect('cart_login_error')

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart.objects.filter(session_key=session_key, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(session_key=session_key, product=product, quantity=1)

    return redirect('view_cart')

# Increase quantity
def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1

    request.session['cart'] = cart
    return redirect('view_cart')

# Decrease quantity
def subtract_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]

    request.session['cart'] = cart
    return redirect('view_cart')

# Update quantity
def update_cart_quantity(request, product_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart_item = Cart.objects.filter(session_key=session_key, product_id=product_id).first()

        if cart_item:
            if action == 'increase' and cart_item.quantity < 20:  # Max quantity 20
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:  # Min quantity 1
                cart_item.quantity -= 1

            cart_item.save()

    return redirect('view_cart')

# Remove item
def remove_from_cart(request, item_id):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_item = Cart.objects.filter(session_key=session_key, product_id=item_id).first()
    if cart_item:
        cart_item.delete()

    return redirect('view_cart')















# Wishlist views
from .models import Wishlist

def get_session_key(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    return session_key

def wishlist_view(request):
    # Check if user is logged in via session
    if 'user_id' not in request.session:
        return redirect('cart_login_error')

    session_key = get_session_key(request)
    wishlist_items = Wishlist.objects.filter(session_key=session_key)

    # Count distinct wishlist items
    wishlist_count = wishlist_items.count()

    return render(request, 'cart/wishlist.html', {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count,  # pass count here
    })


def add_to_wishlist(request, product_id):
    if 'user_id' not in request.session:
        return redirect('cart_login_error')

    session_key = get_session_key(request)
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(session_key=session_key, product=product)

    return redirect('wishlist')


def remove_from_wishlist(request, product_id):
    # Check if user is logged in via session
    if 'user_id' not in request.session:
        return redirect('cart_login_error')

    session_key = get_session_key(request)
    Wishlist.objects.filter(session_key=session_key, product_id=product_id).delete()
    return redirect('wishlist')

