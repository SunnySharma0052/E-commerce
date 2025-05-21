# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('product_detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('categories/', views.category_listing, name='category_listing'),  # Added category_listing here
    path('search/', views.search_results, name='search_results'),
    path('increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:product_id>/', views.subtract_from_cart, name='decrease_quantity'),
    path('update/<int:product_id>/', views.update_cart_quantity, name='update_quantity'),
]
