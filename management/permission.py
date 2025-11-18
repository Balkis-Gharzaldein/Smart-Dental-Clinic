from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user  and  request.user.is_staff)
    
class IsLaboratory(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user  and  request.user.is_staff)  