from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(StoreCategory)
class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'img', 'url')
    search_fields = ('name', 'description')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'get_package_name', 'store_category_id', 'store_name', 'get_payment_status')
    search_fields = ('store_name', 'user_id__username')
    list_filter = ('store_category_id',)

    def get_package_name(self, obj):
        return obj.package_id.name if obj.package_id else "-"
    
    get_package_name.short_description = "Package"

    def get_payment_status(self, obj):
        return obj.payment_id.status if obj.payment_id else "No Payment"
    
    get_payment_status.short_description = "Payment Status"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_store_name', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('store_id__store_name',)

    def get_store_name(self, obj):
        return obj.store_id.store_name if obj.store_id else "-"
    
    get_store_name.short_description = "Store"

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'message', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('user_id__username', 'message')
