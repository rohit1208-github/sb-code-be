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
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'role_name', 
                  'country', 'country_name', 'branch', 'branch_name', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data.get('password', User.objects.make_random_password()),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role'),
            country=validated_data.get('country'),
            branch=validated_data.get('branch')
        )
        return user
    

