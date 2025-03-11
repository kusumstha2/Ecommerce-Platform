import json
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import StoreCategory, Package, Theme, Store, Payment, Notification
from .serializers import (
    StoreCategorySerializer, PackageSerializer, ThemeSerializer, 
    StoreSerializer, PaymentSerializer, NotificationSerializer
)
from User.models import User  

# Generic function to handle caching
def get_or_set_cache(cache_key, queryset, serializer_class, timeout=60*15):
    data = cache.get(cache_key)

    if data is None:
        print(f"Fetching {cache_key} from Database...")
        serialized_data = serializer_class(queryset, many=True).data
        cache.set(cache_key, json.dumps(serialized_data), timeout)
        return serialized_data
    else:
        print(f"Fetching {cache_key} from Cache...")
        return json.loads(data)

class StoreCategoryViewSet(viewsets.ModelViewSet):
    queryset = StoreCategory.objects.all()
    serializer_class = StoreCategorySerializer

    def list(self, request, *args, **kwargs):
        return Response(get_or_set_cache("all_store_categories", self.queryset, self.serializer_class))

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"store_category_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, StoreCategory.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        serializer.save()
        cache.delete("all_store_categories")  # Invalidate cache

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def list(self, request, *args, **kwargs):
        return Response(get_or_set_cache("all_packages", self.queryset, self.serializer_class))

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"package_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, Package.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        package = serializer.save()
        cache.delete("all_packages")  # Invalidate cache after new package creation

        # Email Notification
        user_id = self.request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)

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
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

    def list(self, request, *args, **kwargs):
        return Response(get_or_set_cache("all_themes", self.queryset, self.serializer_class))

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"theme_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, Theme.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        serializer.save()
        cache.delete("all_themes")  # Invalidate cache

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def list(self, request, *args, **kwargs):
        return Response(get_or_set_cache("all_stores", self.queryset, self.serializer_class))

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"store_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, Store.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        serializer.save()
        cache.delete("all_stores")

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request, *args, **kwargs):
        return Response(get_or_set_cache("all_payments", self.queryset, self.serializer_class))

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"payment_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, Payment.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        serializer.save()
        cache.delete("all_payments")

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request, *args, **kwargs):
        return Response(get_or_set_cache("all_notifications", self.queryset, self.serializer_class))

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"notification_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, Notification.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        serializer.save()
        cache.delete("all_notifications")  # Invalidate cache after creating a notification
