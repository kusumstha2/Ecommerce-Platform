from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'gender', 'phone', 'store_name', 'store_description', 'store_logo']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data.get('username'),
            gender=validated_data.get('gender'),
            phone=validated_data.get('phone'),
            store_name=validated_data.get('store_name'),
            store_description=validated_data.get('store_description'),
            store_logo=validated_data.get('store_logo'),
            is_active=True  # Ensure user is active
        )
        user.set_password(validated_data['password'])
        user.save()

        # Assign End User role by default
        end_user_group, created = Group.objects.get_or_create(name='End User')
        user.role = end_user_group
        user.groups.add(end_user_group)
        user.save()

        return user

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
from rest_framework import serializers

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()  # Expecting the refresh token as a string
    
