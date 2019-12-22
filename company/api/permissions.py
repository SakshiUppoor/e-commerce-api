from rest_framework.permissions import BasePermission, SAFE_METHODS

from customer.models import User


class IsAdminUser(BasePermission):
    message = "You must be an admin"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff == True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff == True


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of the company"

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_company and obj.username == request.user.username


class IsCompany(BasePermission):
    message = "You must be a company"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_company

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_company


class IsProductOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of the product"

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.company == request.user


class IsCustomer(BasePermission):
    message = "You must be a customer"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_customer

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_customer


class IsCartOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of the cart"

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.cart.user == request.user


class IsWishlistOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of the wishlist"

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.wishlist.user == request.user


class IsOrderOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of the order"

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.order.cart.user == request.user
