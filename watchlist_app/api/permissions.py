from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # Check if the request method is GET (read-only)
        if request.method == 'GET':
            return True
        # Otherwise, check if the user is an admin
        else:
            return bool(request.user and request.user.is_staff)



#this is used to review the permisssion of the review made by the user
class IsReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the request method is in SAFE_METHODS (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # For write operations (POST, PUT, DELETE), allow access only if the user matches obj.review_user
        else:
            return obj.review_user == request.user or request.user.is_staff
