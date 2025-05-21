from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('success/', views.order_success_view, name='order_success'),
    path('add-address/', views.add_address_view, name='add_address'),  # ✅ This fixes your error
    path('address-list/', views.address_list_view, name='address_list'),
    path('remove-address/<int:address_id>/', views.remove_address_view, name='remove_address'),
    path('update-address/<int:address_id>/', views.update_address_view, name='update_address'),


    path('checkout/login/', views.checkout_login_step, name='checkout_login_step'),
    path('checkout/change-login/', views.change_login, name='change_login'),

    path('checkout/update_quantity/<int:product_id>/', views.checkout_update_quantity, name='checkout_update_quantity'),
    path('checkout/increase/<int:product_id>/', views.checkout_increase_quantity, name='checkout_increase_quantity'),
    path('checkout/decrease/<int:product_id>/', views.checkout_decrease_quantity, name='checkout_decrease_quantity'),
    path('checkout/remove/<int:product_id>/', views.checkout_remove_item, name='checkout_remove_item'),

]

