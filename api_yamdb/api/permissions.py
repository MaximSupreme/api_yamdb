from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminModeratorAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        return (
            request.user.is_authenticated and (
                request.user == obj.author
                or request.user.is_moderator
                or request.user.is_admin
            )
        )


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin)


class IsAdmin(BasePermission):
    message = 'Access is allowed only to administrators.'
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_admin or request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    message = 'Content modification is available only for administrators.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return request.user.is_admin or request.user.is_superuser


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)
