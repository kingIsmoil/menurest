from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOrderOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
    

class CanDeactivateOrder(BasePermission):
    """Проверяет право на деактивацию заказа"""
    def has_permission(self, request, view):
        return request.user.has_perm('orders.can_deactivate_order')

class CanViewAllOrders(BasePermission):
    """Проверяет право на просмотр всех заказов"""
    def has_permission(self, request, view):
        return request.user.has_perm('orders.can_view_all_orders')

