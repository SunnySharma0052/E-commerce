from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Product_Detail  # Ensure both are imported
from cart.models import Cart  # Assuming you have a Cart model


# Create your views here.

# View for the product detail page
from django.shortcuts import render, get_object_or_404
from .models import Product, Product_Detail
from cart.models import Cart  # adjust import if needed

def product_detail(request, slug):
    # Get the main product and its detailed info
    product = get_object_or_404(Product, slug=slug)
    product_detail = get_object_or_404(Product_Detail, product=product)

    # Extract size and color options if available
    size_options = product_detail.size.split(",") if product_detail.size else []
    color_options = product_detail.color.split(",") if product_detail.color else []

    # Recently viewed products logic with session
    recently_viewed = request.session.get('recently_viewed', [])

    # Avoid duplicates: remove and add to front
    if product.id in recently_viewed:
        recently_viewed.remove(product.id)
    recently_viewed.insert(0, product.id)

    # Keep only latest 10 items
    recently_viewed = recently_viewed[:10]
    request.session['recently_viewed'] = recently_viewed

    # Get queryset of recently viewed products maintaining order
    recently_viewed_products = Product.objects.filter(id__in=recently_viewed)
    recently_viewed_products = sorted(
        recently_viewed_products,
        key=lambda x: recently_viewed.index(x.id)
    )

    # Get or create session key for cart
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # Get cart item for this product and session if exists
    cart_item = Cart.objects.filter(session_key=session_key, product=product).first()

    context = {
        'product': product,
        'product_detail': product_detail,
        'size_options': size_options,
        'color_options': color_options,
        'recently_viewed': recently_viewed_products,
        'cart_item': cart_item,  # pass cart item for quantity display
    }

    return render(request, 'products/product_detail.html', context)





def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    # Name match karke products filter karo
    products = Product.objects.filter(
        category__name=category.name,  # Category ka name match
        is_available=True              # Aur available bhi ho
    )

    return render(request, 'products/category_detail.html', {
        'category': category,
        'products': products
    })





def category_listing(request):
    categories = Category.objects.all()

    # Handle search filter
    search_query = request.GET.get('search', '')
    if search_query:
        categories = categories.filter(name__icontains=search_query)

    # Handle price filters (assuming your products have price fields)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        categories = categories.filter(product__price__gte=min_price, product__price__lte=max_price)

    # Handle rating filter (assuming you have a rating field in products)
    rating = request.GET.get('rating')
    if rating:
        categories = categories.filter(product__rating__gte=rating)

    return render(request, 'products/category_listing.html', {'categories': categories})




def search_results(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'products/search_results.html', {'query': query, 'results': results})





# Increase quantity
def increase_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1

    request.session['cart'] = cart
    return redirect('product_detail', slug=product.slug)

# Decrease quantity
def subtract_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]

    request.session['cart'] = cart
    return redirect('product_detail', slug=product.slug)

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
            if action == 'increase' and cart_item.quantity < 20:
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1
            cart_item.save()

        product = get_object_or_404(Product, id=product_id)
        return redirect('product_detail', slug=product.slug)

    return redirect('home')
