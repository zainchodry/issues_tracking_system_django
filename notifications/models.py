from django.conf import settings
from django.db import models


class Notification(models.Model):

    class NotificationType(models.TextChoices):

        PROJECT = "PROJECT", "Project"

        ISSUE = "ISSUE", "Issue"

        COMMENT = "COMMENT", "Comment"

        SYSTEM = "SYSTEM", "System"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(
        max_length=255,
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
    )

    is_read = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    read_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return self.title
    
class NotificationPreference(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preferences",
    )

    email_notifications = models.BooleanField(
        default=True,
    )

    browser_notifications = models.BooleanField(
        default=True,
    )

    issue_assignment = models.BooleanField(
        default=True,
    )

    issue_updates = models.BooleanField(
        default=True,
    )

    project_updates = models.BooleanField(
        default=True,
    )

    comment_notifications = models.BooleanField(
        default=True,
    )

    def __str__(self):

        return self.user.username
    
class EmailLog(models.Model):

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    subject = models.CharField(
        max_length=255,
    )

    status = models.CharField(
        max_length=50,
        default="Pending",
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):

        return self.subject
