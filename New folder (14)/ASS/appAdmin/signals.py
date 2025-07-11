from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import AdminPanelLoginHistory

@receiver(user_logged_in)
def log_admin_login(sender, request, user, **kwargs):
    if request.path.startswith('/admin/'):
        AdminPanelLoginHistory.objects.create(
            user=user,
            date_time=timezone.now(),
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            is_logged_in=True,
            action='login'
        )

@receiver(user_logged_out)
def log_admin_logout(sender, request, user, **kwargs):
    if request and request.path.startswith('/admin/'):
        AdminPanelLoginHistory.objects.create(
            user=user,
            date_time=timezone.now(),
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            is_logged_in=False,
            action='logout'
        ) 