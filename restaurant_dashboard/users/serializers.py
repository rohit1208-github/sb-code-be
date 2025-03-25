# users/serializers.py
from rest_framework import serializers
from .models import User, UserRole

class UserRoleSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    
    class Meta:
        model = UserRole
        fields = ['id', 'name', 'name_display', 'description']

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.get_name_display', read_only=True)
    country_name = serializers.CharField(source='country.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'description',
                  'role', 'role_name', 'country', 'country_name', 'branch', 'branch_name', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'role': {'required': True},
            'phone': {'required': False},
            'description': {'required': False},
            'country': {'required': False},
            'branch': {'required': False},
            'is_active': {'required': False},
        }
    
    def validate(self, data):
        # Ensure the required fields are present
        if not data.get('first_name'):
            raise serializers.ValidationError({'first_name': 'First name is required'})
        if not data.get('last_name'):
            raise serializers.ValidationError({'last_name': 'Last name is required'})
        if not data.get('role'):
            raise serializers.ValidationError({'role': 'Role is required'})
        if not data.get('email'):
            raise serializers.ValidationError({'email': 'Email is required'})
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data.get('password', User.objects.make_random_password()),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            description=validated_data.get('description', ''),
            role=validated_data.get('role'),
            country=validated_data.get('country'),
            branch=validated_data.get('branch'),
            is_active=validated_data.get('is_active', True)  # Status field (default active)
        )
        return user    

