from rest_framework.permissions import BasePermission

class IsProjectCoordinator(BasePermission):
    """
    Allows access only to users in the Project_Coordinator group.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.groups.filter(name='Project_Coordinator').exists()
        )

class IsSupervisor(BasePermission):
    """
    Allows access only to users in the Supervisor group.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.groups.filter(name='Supervisor').exists()
        )

class IsStudent(BasePermission):
    """
    Allows access only to users in the Student group.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.groups.filter(name='Student').exists()
        )