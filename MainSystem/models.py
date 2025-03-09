from django.db import models
from User.models import *
from datetime import timedelta, datetime
from django.conf import settings
# Create your models here.
from django.utils import timezone

from django.db import models

from datetime import timedelta

from datetime import datetime, timedelta
from django.db import models



class StoreCategory(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name

class Package(models.Model):
    BASIC = 'basic'
    PREMIUM = 'premium'
    ENTERPRISE = 'enterprise'

    PACKAGE_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (ENTERPRISE, 'Enterprise'),
    ]

    PACKAGE_DURATIONS = {
        BASIC: ("1 Month", timedelta(days=30)),
        PREMIUM: ("3 Months", timedelta(days=90)),
        ENTERPRISE: ("1 Year", timedelta(days=365)),
    }

    PACKAGE_PRICES = {
        BASIC: 1000, 
        PREMIUM: 1500, 
        ENTERPRISE: 2000,  
    }
    
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="packages", null=True, blank=True)
    name = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    duration = models.CharField(max_length=20, blank=True)  # Store as text
    expiry_date = models.DateTimeField(null=True, blank=True, default=datetime.now)  # Use callable for default
    package_type = models.CharField(max_length=10, choices=PACKAGE_CHOICES, default=BASIC)
    features = models.TextField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Set duration text and expiry date based on package type
        duration_text, duration_timedelta = self.PACKAGE_DURATIONS.get(self.package_type, ("1 Month", timedelta(days=30)))
        self.duration = duration_text
        self.expiry_date = timezone.now() + duration_timedelta  # Use timezone-aware datetime

        # Set price based on package type
        self.price = self.PACKAGE_PRICES.get(self.package_type, 29.99)  # Default price for Basic

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.duration})"



    
    
class Theme(models.Model):
    name = models.CharField(max_length=225)
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE,default=1)
    description = models.TextField()
    img = models.ImageField(upload_to='theme_images/', null=True, blank=True)
    url = models.URLField(max_length=225) 

    def __str__(self):
        return self.name




class Store(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    themes = models.ManyToManyField(Theme)  # Allow multiple themes
    store_category_id = models.ForeignKey(StoreCategory, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=300, null=True, blank=True)
    store_description = models.TextField(null=True, blank=True)
    store_logo = models.ImageField(upload_to='store_logos/', null=True, blank=True)
    ip=models.CharField(max_length=300, null=True, blank=True)
    domain=models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.store_name if self.store_name else "Unnamed Store"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    store_id = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=225)  # Store payment method info
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically adds timestamp
    
    # Optionally add fields for payment reference, transaction id, etc.
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"

    def mark_as_paid(self):
        """Method to update payment status to 'paid'."""
        self.status = 'paid'
        self.save()

    def mark_as_unpaid(self):
        """Method to update payment status to 'unpaid'."""
        self.status = 'unpaid'
        self.save()

from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=True)

    def __str__(self):
        return f"Notification for {self.user_id.username} - {self.message[:50]}..."  
