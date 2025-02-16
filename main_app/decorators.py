from django.http import JsonResponse
from functools import wraps

def role_required(roles):
    """
    Decorator to restrict access based on user roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=401)
            if request.user.role not in roles:
                return JsonResponse({"error": "Permission denied"}, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator