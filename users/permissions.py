from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение: редактировать и удалять может только владелец.
    Остальные могут только читать, если публичная.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return obj.public or obj.owner == request.user
        # Для небезопасных методов (PUT, DELETE...) — только владелец
        return obj.owner == request.user


# # Владелец
# class IsOwner(permissions.BasePermission):
#     """Является ли пользователь владельцем"""
#
#     def has_object_permission(self, request, view, obj):
#         if obj.owner == request.user:
#             return True
#         return False
