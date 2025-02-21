from rest_framework import serializers
from .models import StoreCategory, Package, Theme, Store, Payment, Notification

class StoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreCategory
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    expiry_date = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Package
        fields = '__all__'

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'



class StoreSerializer(serializers.ModelSerializer):
    themes = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), many=True)  # Accepts multiple IDs

    class Meta:
        model = Store
        fields = '__all__'

    def create(self, validated_data):
        themes = validated_data.pop('themes', [])  # Extract themes from request
        store = Store.objects.create(**validated_data)
        store.themes.set(themes)  # Assign multiple themes
        return store

    def update(self, instance, validated_data):
        themes = validated_data.pop('themes', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if themes is not None:
            instance.themes.set(themes)  # Update themes

        return instance


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
