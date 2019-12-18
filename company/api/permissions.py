from rest_framework.permissions import BasePermission, SAFE_METHODS

from customer.models import User


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of the object"
    my_safe_method = ['GET']

    def has_permissions(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in self.my_safe_method:
            return True
        return obj.username == request.user.username


class IsCompany(BasePermission):
    message = "You must be a company"
    my_safe_method = ['GET']

    def has_permissions(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return bool(request.user and request.user.is_company)

    def has_object_permission(self, request, view, obj):
        if request.method in self.my_safe_method:
            return True
        return bool(request.user and request.user.is_company)


class IsProductOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of the object"
    my_safe_method = ['GET']

    def has_permissions(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in self.my_safe_method:
            return True
        return obj.company == request.user


class IsCustomer(BasePermission):
    def has_permissions(self, request, view):
        return request.user.is_customer == True

    def has_object_permission(self, request, view, obj):
        return request.user.is_customer == True


class IsCartOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of the object"
    my_safe_method = ['GET']

    def has_permissions(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in self.my_safe_method:
            return True
        return obj.cart.user == request.user


class IsCartOwner(BasePermission):
    message = "You must be the owner of the object"
    my_safe_method = []

    def has_permissions(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in self.my_safe_method:
            return True
        return obj.cart.user == request.user


class IsWishlistOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of the object"
    my_safe_method = ['GET']

    def has_permissions(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in self.my_safe_method:
            return True
        return obj.wishlist.user == request.user
