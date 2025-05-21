from django.contrib import admin
from core.admin import *  # This imports all the admin registrations from core
from .models import Product_Detail

# Register your models here.

admin.site.register(Product_Detail)