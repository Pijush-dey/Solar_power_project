from django.utils import timezone
from core.models import UserSession

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            try:
                user_session, created = UserSession.objects.get_or_create(user=user)
                user_session.last_activity = timezone.now()
                if request.session.session_key:
                    user_session.session_key = request.session.session_key
                user_session.save()
            except Exception:
                pass  # Optionally log the error
        return response 