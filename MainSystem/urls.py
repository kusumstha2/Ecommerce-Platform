from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreCategoryViewSet, PackageViewSet, ThemeViewSet, StoreViewSet, PaymentViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'store-categories', StoreCategoryViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'themes', ThemeViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
