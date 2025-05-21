from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, ShippingAddress
from cart.models import Cart, CartItem
from products.models import Product
from django.contrib import messages
from accounts.models import User  # your custom user model
# Create your views here.


# Checkout View
def checkout_view(request):
    # 1. Require login
    if not request.session.get('is_authenticated'):
        messages.warning(request, "Please log in to continue checkout.")
        return redirect('login')

    # 2. Fetch the User
    user = get_object_or_404(User, id=request.session['user_id'])

    # 3. Ensure a session_key exists
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # 4. Load cart items
    cart_qs = Cart.objects.filter(session_key=session_key)
    if not cart_qs.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('view_cart')

    cart_items = []
    total_price = 0
    for ci in cart_qs:
        subtotal = ci.product.price * ci.quantity
        total_price += subtotal
        cart_items.append({
            'product': ci.product,
            'quantity': ci.quantity,
            'subtotal': subtotal,
        })

    # 5. Fetch existing addresses
    user_addresses = ShippingAddress.objects.filter(user=user)

    # 6. Handle form submission
    if request.method == 'POST':
        addr_id = request.POST.get('address')
        if addr_id:
            # Use an existing address
            shipping = get_object_or_404(ShippingAddress, id=addr_id, user=user)
        else:
            # Create a new one
            data = {k: request.POST.get(k) for k in
                    ('full_name','phone','address','city','state','zip_code','country')}
            if not all(data.values()):
                messages.error(request, "Fill all address fields or select an existing one.")
                return render(request, 'checkout/checkout.html', {
                    'cart_items': cart_items,
                    'total_price': total_price,
                    'user_addresses': user_addresses,
                })
            shipping = ShippingAddress.objects.create(user=user, **data)

        # 7. Create the order
        order = Order.objects.create(
            user=user,
            shipping_address=shipping,
            total_price=total_price,
            is_paid=False,
            payment_method=request.POST.get('payment_method', 'COD'),
        )

        # 8. Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        # 9. Clear the cart
        cart_qs.delete()

        # 10. Redirect to success page
        return redirect('order_success')

    # 11. Render the checkout page
    return render(request, 'checkout/checkout.html', {
        'user': user,
        'cart_items': cart_items,
        'total_price': total_price,
        'user_addresses': user_addresses,
    })

# Order Success View
def order_success_view(request):
    # Optional: Clear cart again on success page just in case
    if request.session.session_key:
        Cart.objects.filter(session_key=request.session.session_key).delete()

    return render(request, 'checkout/order_success.html')






# Add New Address View
def add_address_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/accounts/login/?next=/checkout/')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')

        if all([full_name, phone, address, city, state, zip_code, country]):
            ShippingAddress.objects.create(
                user=user,
                full_name=full_name,
                phone=phone,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                country=country
            )
            messages.success(request, "Address saved successfully!")
            return redirect('checkout')  # ✅ redirect to show saved address
        else:
            context = {"error": "All fields are required."}
            return render(request, 'checkout/add_address.html', context)

    return render(request, 'checkout/add_address.html')

# Address List View (Show all addresses for user)
def address_list_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/accounts/login/?next=/checkout/')
    
    user = get_object_or_404(User, id=user_id)
    addresses = ShippingAddress.objects.filter(user=user)

    return render(request, 'checkout/address_list.html', {
        'addresses': addresses,
    })

# Remove Address View
def remove_address_view(request, address_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/accounts/login/?next=/checkout/')
    user = get_object_or_404(User, id=user_id)
    address = get_object_or_404(ShippingAddress, id=address_id, user=user)
    address.delete()
    return redirect('address_list')

# Update Address View
def update_address_view(request, address_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/accounts/login/?next=/checkout/')
    user = get_object_or_404(User, id=user_id)
    address = get_object_or_404(ShippingAddress, id=address_id, user=user)

    if request.method == 'POST':
        address.full_name = request.POST['full_name']
        address.phone = request.POST['phone']
        address.address = request.POST['address']
        address.city = request.POST['city']
        address.state = request.POST['state']
        address.zip_code = request.POST['zip_code']
        address.country = request.POST['country']
        address.save()
        return redirect('address_list')

    return render(request, 'checkout/update_address.html', {'address': address})








# checkout_login_step view
def checkout_login_step(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/accounts/login/?next=/checkout/')

    user = get_object_or_404(User, id=user_id)

    context = {
        'user': user,
    }
    return render(request, 'checkout_login_step.html', context)

# change_login view
def change_login(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/accounts/login/?next=/checkout/')







# update_checkout_quantity view
def checkout_update_quantity(request, product_id):
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
                cart_item.save()
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()

    return redirect('checkout')



# Increase quantity for checkout
def checkout_increase_quantity(request, product_id):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_item = Cart.objects.filter(session_key=session_key, product_id=product_id).first()
    if cart_item and cart_item.quantity < 20:  # max limit 20
        cart_item.quantity += 1
        cart_item.save()

    return redirect('checkout')  # Your checkout page url name

# Decrease quantity for checkout
def checkout_decrease_quantity(request, product_id):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_item = Cart.objects.filter(session_key=session_key, product_id=product_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # Remove if quantity <= 1 and user wants to decrease
            cart_item.delete()

    return redirect('checkout')

# Remove item from checkout
def checkout_remove_item(request, product_id):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_item = Cart.objects.filter(session_key=session_key, product_id=product_id).first()
    if cart_item:
        cart_item.delete()

    return redirect('checkout')
