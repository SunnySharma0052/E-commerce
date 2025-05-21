from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_featured_categories = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    discount_end_time = models.DateTimeField(blank=True, null=True)

    # Ratings
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    # Image
    image = models.ImageField(upload_to='products/', default='products/default.jpg')

    # Availability & metadata
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_popular = models.BooleanField(default=False)
    is_daily_best_sell = models.BooleanField(default=False)


    def __str__(self):
        return self.name
