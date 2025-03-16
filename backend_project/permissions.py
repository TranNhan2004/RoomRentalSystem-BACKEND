from rest_framework.permissions import BasePermission


# -----------------------------------------------------------
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'MANAGER'
    
        
# -----------------------------------------------------------
class IsLessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'LESSOR'
    
    
# -----------------------------------------------------------
class IsRenter(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'RENTER'
    

# -----------------------------------------------------------
class IsRenterOrLessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'RENTER' or request.user.role == 'LESSOR'