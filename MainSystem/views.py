from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import StoreCategory, Package, Theme, Store, Payment, Notification
from .serializers import StoreCategorySerializer, PackageSerializer, ThemeSerializer, StoreSerializer, PaymentSerializer, NotificationSerializer

# StoreCategory ViewSet
class StoreCategoryViewSet(viewsets.ModelViewSet):
    queryset = StoreCategory.objects.all()
    serializer_class = StoreCategorySerializer

# Package ViewSetfrom django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import viewsets
from .models import Package
from .serializers import PackageSerializer
from django.shortcuts import get_object_or_404
from User.models import User  # Assuming you have the User model imported

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def perform_create(self, serializer):
        # Save the package instance
        package = serializer.save()

        # Assuming the user ID is passed with the request and is related to the package
        user_id = self.request.data.get("user_id")  # Make sure the user_id is passed in the request
        user = get_object_or_404(User, id=user_id)

        # Prepare the email content
        subject = "Package Purchase Confirmation"
        message = f"""
        Dear {user.username},

        Thank you for purchasing the '{package.name}' package!

        Your package details:
        - Package Name: {package.name}
        - Price: ${package.price}
        - Duration: {package.duration}
        - Expiry Date: {package.expiry_date.strftime('%Y-%m-%d %H:%M:%S')}

        You can now access your package features.

        Best Regards,  
        Mindriser Tech
        """
        
        # Send the email to the user
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

# Theme ViewSet
class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

# Store ViewSet
class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

# Payment ViewSet
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# Notification ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
