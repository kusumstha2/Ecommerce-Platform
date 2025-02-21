from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import StoreCategory, Package, Theme, Store, Payment, Notification
from .serializers import StoreCategorySerializer, PackageSerializer, ThemeSerializer, StoreSerializer, PaymentSerializer, NotificationSerializer

# StoreCategory ViewSet
class StoreCategoryViewSet(viewsets.ModelViewSet):
    queryset = StoreCategory.objects.all()
    serializer_class = StoreCategorySerializer

# Package ViewSet
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

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
