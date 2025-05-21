from django.db import models
from core.models import Category, Product  # Import Product from core

# Create your models here.
class Product_Detail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    # New Category Field
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_details')


    # Descriptions
    short_description = models.TextField()
    long_description = models.TextField()

    # NEW FIELDS (as per your request)
    color = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    product_code = models.CharField(max_length=100, blank=True, null=True)
    availability_text = models.CharField(max_length=100, default="In Stock")
    product_type = models.CharField(max_length=100, blank=True, null=True)
    shipping_time = models.CharField(max_length=100, default="02 day shipping")

    # General product info
    unit = models.CharField(max_length=100, blank=True, null=True)
    seller_name = models.CharField(max_length=200, blank=True, null=True)
    storage_tips = models.TextField(blank=True, null=True)

    # Detailed information fields
    weight = models.CharField(max_length=100, blank=True, null=True)
    ingredient_type = models.CharField(max_length=200, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    package_quantity = models.CharField(max_length=100, blank=True, null=True)
    form = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    net_quantity = models.CharField(max_length=100, blank=True, null=True)
    dimensions = models.CharField(max_length=200, blank=True, null=True)

    # Metadata-type details
    asin = models.CharField(max_length=100, blank=True, null=True)
    best_sellers_rank = models.CharField(max_length=200, blank=True, null=True)
    date_first_available = models.DateField(blank=True, null=True)
    item_weight = models.CharField(max_length=100, blank=True, null=True)
    generic_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.product.name
