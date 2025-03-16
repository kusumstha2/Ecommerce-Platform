import json
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.conf import settings
from .models import StoreCategory, Package, Theme, Store, Payment, Notification
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .serializers import (
    StoreCategorySerializer, PackageSerializer, ThemeSerializer, 
    StoreSerializer, PaymentSerializer, NotificationSerializer
)
from User.models import User  
from User.models import User  
from .task import send_package_email

def get_or_set_cache(cache_key, queryset, serializer_class, timeout=60*15):
    """
    Fetch data from cache or set cache if not available.
    If data is not found in cache, it is fetched from the database
    and cached for subsequent requests.
    """
    data = cache.get(cache_key)

    if data is None:
        print(f"Fetching {cache_key} from Database...")
        # Fetch data from the database if not in cache
        serialized_data = serializer_class(queryset, many=True).data
        # Set cache
        cache.set(cache_key, json.dumps(serialized_data), timeout)
        return serialized_data
    else:
        print(f"Fetching {cache_key} from Cache...")
        # Return data from cache if available
        return json.loads(data)

def invalidate_cache(cache_key):
    """
    Invalidate a specific cache key.
    """
    cache.delete(cache_key)
    print(f"Cache invalidated for key: {cache_key}")

class StoreCategoryViewSet(viewsets.ModelViewSet):
    queryset = StoreCategory.objects.all()
    serializer_class = StoreCategorySerializer
 

    def list(self, request, *args, **kwargs):
        query = request.GET.get("q", None)
        cache_key = f"store_search_{query}" if query else "all_stores"

        # Check cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(json.loads(cached_data))

        # Full-text search in PostgreSQL
        if query:
            search_results = Store.objects.annotate(
                search=SearchVector("name", "description")
            ).filter(search=SearchQuery(query))
        else:
            search_results = self.queryset

        serialized_data = StoreSerializer(search_results, many=True).data
        cache.set(cache_key, json.dumps(serialized_data), timeout=60 * 15)

        return Response(serialized_data)
    
    def retrieve(self, request, *args, **kwargs):
        cache_key = f"store_category_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, StoreCategory.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        serializer.save()
        invalidate_cache("all_store_categories")  # Invalidate cache after creating a new store category

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    
 

    def list(self, request, *args, **kwargs):
        query = request.GET.get("q", None)
        cache_key = f"package_search_{query}" if query else "packages"

        if query:
            search_results = Package.objects.annotate(
                search=SearchVector("name", "description")
            ).filter(search=SearchQuery(query))
        else:
            search_results = self.queryset

        return Response(get_or_set_cache(cache_key, search_results, self.serializer_class))

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"package_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, Package.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        package = serializer.save()
        cache.delete("all_packages")  # Invalidate cache after new package creation

        # Get user ID
        user_id = self.request.data.get("user_id")

        # Send email asynchronously using Celery
        send_package_email.delay(
            user_id,
            package.name,
            package.price,
            package.duration,
            package.expiry_date.strftime('%Y-%m-%d %H:%M:%S')
        )


        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

    



    def list(self, request, *args, **kwargs):
        query = request.GET.get("q", None)
        cache_key = f"theme_search_{query}" if query else "themes"

        if query:
            search_results = Theme.objects.annotate(
                search=SearchVector("name", "description")
            ).filter(search=SearchQuery(query))
        else:
            search_results = self.queryset

        return Response(get_or_set_cache(cache_key, search_results, self.serializer_class))

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"theme_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, Theme.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        serializer.save()
        invalidate_cache("all_themes")  # Invalidate cache after creating a new theme

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    
  
    def list(self, request, *args, **kwargs):
        query = request.GET.get("q", None)
        cache_key = f"store_search_{query}" if query else "stores"

        if query:
            search_results = Store.objects.annotate(
                search=SearchVector("name", "description")
            ).filter(search=SearchQuery(query))
        else:
            search_results = self.queryset

        return Response(get_or_set_cache(cache_key, search_results, self.serializer_class))

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"store_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, Store.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        serializer.save()
        invalidate_cache("all_stores")  # Invalidate cache after creating a new store

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
   
   

    def list(self, request, *args, **kwargs):
        query = request.GET.get("q", None)
        cache_key = f"payment_search_{query}" if query else "payments"

        if query:
            search_results = Payment.objects.annotate(
                search=SearchVector("payment_id", "amount")
            ).filter(search=SearchQuery(query))
        else:
            search_results = self.queryset

        return Response(get_or_set_cache(cache_key, search_results, self.serializer_class))
    
    def retrieve(self, request, *args, **kwargs):
        cache_key = f"payment_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, Payment.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        serializer.save()
        invalidate_cache("all_payments")  # Invalidate cache after creating a new payment

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
 
    

    def list(self, request, *args, **kwargs):
        query = request.GET.get("q", None)
        cache_key = f"notification_search_{query}" if query else "notifications"

        if query:
            search_results = Notification.objects.annotate(
                search=SearchVector("title", "message")
            ).filter(search=SearchQuery(query))
        else:
            search_results = self.queryset

        return Response(get_or_set_cache(cache_key, search_results, self.serializer_class))
    
    def retrieve(self, request, *args, **kwargs):
        cache_key = f"notification_{kwargs.get('pk')}"
        return Response(get_or_set_cache(cache_key, Notification.objects.filter(pk=kwargs.get('pk')), self.serializer_class))

    def perform_create(self, serializer):
        serializer.save()
        invalidate_cache("all_notifications")  # Invalidate cache after creating a new notification
