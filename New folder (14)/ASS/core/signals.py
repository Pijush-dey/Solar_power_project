from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from core.models import UserSession

User = get_user_model()

@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    try:
        UserSession.objects.get(user=user).delete()
    except UserSession.DoesNotExist:
        pass

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    # Remove any previous session for this user
    try:
        user_session = UserSession.objects.get(user=user)
        if user_session.session_key != request.session.session_key:
            # Delete the old session
            Session.objects.filter(session_key=user_session.session_key).delete()
            user_session.delete()
    except UserSession.DoesNotExist:
        pass
    # Create new session record
    UserSession.objects.update_or_create(
        user=user,
        defaults={
            'session_key': request.session.session_key,
            'last_activity': timezone.now(),
        }
    ) 