##
from functools import wraps

from django.http import JsonResponse


def get_user_from_header(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_email = request.headers.get('X-Consumer-Custom-Id')
        print(user_email)
        if not user_email:
            return JsonResponse({'error': 'X-Consumer-Custom-Id header is missing'}, status=400)

        request.user = user_email
        return view_func(request, *args, **kwargs)

    return _wrapped_view
