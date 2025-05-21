from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.EmailField(unique=True, default="Not Provided")
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField(max_length=80, null=True, blank=True, default="Not Provided")
    password = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profile_images/', default="defaultprofilepic.jpg", blank=True)

    # Extra fields
    password_reset_code = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email_id})"


class DeletedAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="deletion_info")
    deleted_at = models.DateTimeField(auto_now_add=True)
    is_permanently_deleted = models.BooleanField(default=False)

    def days_remaining(self):
        """Return number of days left before permanent deletion."""
        expiration = self.deleted_at + timedelta(days=30)
        return max((expiration - timezone.now()).days, 0)

    def is_expired(self):
        """Check if 30 days passed since deletion."""
        return timezone.now() > self.deleted_at + timedelta(days=30)

    def __str__(self):
        return f"Deleted: {self.user.email_id} on {self.deleted_at.strftime('%Y-%m-%d')}"
