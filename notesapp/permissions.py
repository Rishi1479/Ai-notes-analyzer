from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    """Allow access only to users with role='teacher'."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsStudent(BasePermission):
    """Allow access only to users with role='student'."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsAdminUser(BasePermission):
    """Allow access only to users with role='admin'."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsTeacherOrAdmin(BasePermission):
    """Allow access to teachers and admins."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('teacher', 'admin')


class IsOwner(BasePermission):
    """Object-level permission: only the uploader can modify."""

    def has_object_permission(self, request, view, obj):
        return obj.uploaded_by == request.user
