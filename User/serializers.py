from rest_framework import serializers
from .models import User  # Ensure this is your custom User model
from django.contrib.auth.models import Group

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone']  # Removed 'username' since it's optional in the User model

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            phone=validated_data.get('phone'),
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




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()  # Expecting the refresh token as a string