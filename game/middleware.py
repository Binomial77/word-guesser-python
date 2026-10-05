from django.db import OperationalError, ProgrammingError
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse

from .models import User
from .services import seed_data

PUBLIC_PATHS = {'/', '/login', '/register', '/api/auth/login', '/api/auth/register', '/favicon.ico'}
_seeded = False


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def _ensure_seed(self):
        global _seeded
        if _seeded:
            return
        try:
            seed_data()
            _seeded = True
        except (OperationalError, ProgrammingError):
            pass  # tables not created yet; retry on next request

    def __call__(self, request):
        self._ensure_seed()
        path = request.path

        # Attach the user (if logged in) on every request, including public pages.
        request.current_user = None
        uid = request.session.get('user_id')
        if uid:
            try:
                request.current_user = User.objects.get(id=uid)
            except User.DoesNotExist:
                request.session.flush()

        if path in PUBLIC_PATHS or path.startswith('/static/'):
            return self.get_response(request)

        user = request.current_user
        is_api = path.startswith('/api/')
        if not user:
            if is_api:
                return JsonResponse({'message': 'Please log in'}, status=401)
            return HttpResponseRedirect('/login')

        if (path == '/admin' or path.startswith('/api/admin')) and user.role != 'ADMIN':
            if is_api:
                return JsonResponse({'message': 'Admin access required'}, status=403)
            return HttpResponseForbidden('Admin access required')
        return self.get_response(request)
