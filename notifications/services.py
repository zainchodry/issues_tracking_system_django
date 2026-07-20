from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Notification,
    EmailLog,
)

class NotificationService:

    @staticmethod
    def create_notification(
        recipient,
        title,
        message,
        notification_type,
    ):

        notification = Notification.objects.create(

            recipient=recipient,

            title=title,

            message=message,

            notification_type=notification_type,

        )

        return notification
    
    @staticmethod
    def mark_as_read(
        notification,
    ):

        notification.is_read = True

        notification.read_at = timezone.now()

        notification.save(
            update_fields=[
                "is_read",
                "read_at",
            ]
        )

        return notification
    
    @staticmethod
    def mark_all_as_read(
        user,
    ):

        Notification.objects.filter(

            recipient=user,

            is_read=False,

        ).update(

            is_read=True,

            read_at=timezone.now(),

        )

    @staticmethod
    def delete_notification(
        notification,
    ):

        notification.delete()

    @staticmethod
    def send_issue_assignment_notification(
        issue,
    ):

        if not issue.assignee:

            return

        NotificationService.create_notification(

            recipient=issue.assignee,

            title="Issue Assigned",

            message=(
                f"You have been assigned "
                f"issue '{issue.title}'."
            ),

            notification_type=Notification.NotificationType.ISSUE,

        )

    @staticmethod
    def send_project_member_notification(
        member,
    ):

        NotificationService.create_notification(

            recipient=member.user,

            title="Added to Project",

            message=(
                f"You were added to "
                f"{member.project.name}."
            ),

            notification_type=Notification.NotificationType.PROJECT,

        )

    @staticmethod
    def send_status_notification(
        issue,
        old_status,
    ):

        if not issue.assignee:

            return

        NotificationService.create_notification(

            recipient=issue.assignee,

            title="Issue Status Updated",

            message=(
                f"Status changed "
                f"from '{old_status}' "
                f"to '{issue.status}'."
            ),

            notification_type=Notification.NotificationType.ISSUE,

        )

    @staticmethod
    def send_email(

        recipient,

        subject,

        message,

    ):

        log = EmailLog.objects.create(

            recipient=recipient,

            subject=subject,

            status="Pending",

        )

        try:

            send_mail(

                subject,

                message,

                settings.DEFAULT_FROM_EMAIL,

                [

                    recipient.email,

                ],

                fail_silently=False,

            )

            log.status = "Sent"

            log.sent_at = timezone.now()

            log.save()

        except Exception:

            log.status = "Failed"

            log.save()

    @staticmethod
    def notify_with_email(

        recipient,

        title,

        message,

        notification_type,

    ):

        NotificationService.create_notification(

            recipient,

            title,

            message,

            notification_type,

        )

        NotificationService.send_email(

            recipient,

            title,

            message,

        )

