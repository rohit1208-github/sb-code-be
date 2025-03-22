# users/permissions.py
from rest_framework import permissions

class IsLeadershipTeam(permissions.BasePermission):
    """
    Custom permission to only allow leadership team members access.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and has leadership role
        return bool(request.user and request.user.is_authenticated and 
                    request.user.role and request.user.role.name == 'leadership')

class IsCountryLeadership(permissions.BasePermission):
    """
    Custom permission to only allow country leadership team members access.
    """
    def has_permission(self, request, view):
        # Check if user has country leadership role
        return bool(request.user and request.user.is_authenticated and 
                    request.user.role and request.user.role.name == 'country_leadership')
    
    def has_object_permission(self, request, view, obj):
        # Allow access only if object's country matches user's country
        if hasattr(obj, 'country'):
            return obj.country == request.user.country
        
        # If obj has branch that has country
        if hasattr(obj, 'branch') and hasattr(obj.branch, 'country'):
            return obj.branch.country == request.user.country
        
        return False

class IsCountryAdmin(permissions.BasePermission):
    """
    Custom permission to only allow country admin team members access.
    """
    def has_permission(self, request, view):
        # Check if user has country admin role
        return bool(request.user and request.user.is_authenticated and 
                    request.user.role and request.user.role.name == 'country_admin')
    
    def has_object_permission(self, request, view, obj):
        # Allow access only if object's country matches user's country
        if hasattr(obj, 'country'):
            return obj.country == request.user.country
        
        # If obj has branch that has country
        if hasattr(obj, 'branch') and hasattr(obj.branch, 'country'):
            return obj.branch.country == request.user.country
        
        return False

class IsBranchManager(permissions.BasePermission):
    """
    Custom permission to only allow branch managers view access.
    """
    def has_permission(self, request, view):
        # Check if user has branch manager role
        # Read-only for branch managers
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated and 
                        request.user.role and request.user.role.name == 'branch_manager')
        return False
    
    def has_object_permission(self, request, view, obj):
        # Allow view access only if object's branch matches user's branch
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'branch'):
                return obj.branch == request.user.branch
            
            # If obj is a branch
            if obj.__class__.__name__ == 'Branch':
                return obj == request.user.branch
            
            return False
        return False