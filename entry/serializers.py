from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Visitor

# Serializer for Visitor model (for testing protected endpoints)
class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ['id', 'full_name', 'email', 'phone_number', 'purpose', 'host', 'entry_time', 'additional_details']
        read_only_fields = ['entry_time']

# Get the active user model (default or custom)
User = get_user_model()

# Custom Token serializer that accepts email + password and returns tokens
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    This overrides SimpleJWT's TokenObtainPairSerializer to authenticate by email.
    It maps found user's username into attrs['username'] so SimpleJWT can create tokens.
    """
    username_field = 'email'  # tell the base serializer we're using email as the username field

    def validate(self, attrs):
        # attrs will be the incoming data (email, password)
        email = attrs.get('email')
        password = attrs.get('password')

        # Basic validation checks
        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')

        # Try to find the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # If not found, raise error (SimpleJWT expects ValidationError for bad creds)
            raise serializers.ValidationError('Invalid email or password.')

        # Verify password
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password.')

        # Optionally check active
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        # Map to username so super().validate can create tokens normally
        attrs['username'] = user.username

        # Call parent to produce tokens
        data = super().validate(attrs)

        # Optionally, attach user info to response for frontend convenience
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'is_superuser': user.is_superuser,
        }

        return data
