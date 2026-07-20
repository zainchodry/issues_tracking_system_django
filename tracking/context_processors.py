def notifications_count(request):
    """Inject unread notification count into every template."""
    if request.user.is_authenticated:
        from notifications.models import Notification
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_count': count}
    return {'unread_count': 0}
