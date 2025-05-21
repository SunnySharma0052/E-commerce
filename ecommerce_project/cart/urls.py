from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_navbar, name='cart_navbar'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # This is the add to cart URL
  
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/subtract/<int:product_id>/', views.subtract_from_cart, name='subtract_from_cart'),

    path('update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),  # This line adds the update_cart_quantity URL pattern
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart-login-error/', views.cart_login_error, name='cart_login_error'),


    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

]


