from django.db.models.signals import (
    post_save,
    pre_save,
)

from django.dispatch import receiver

from issues.models import Issue

from projects.models import ProjectMember

from accounts.models import User

from .models import (
    NotificationPreference,
)

from .services import NotificationService

@receiver(
    post_save,
    sender=User,
)
def create_notification_preference(
    sender,
    instance,
    created,
    **kwargs,
):

    if created:

        NotificationPreference.objects.create(
            user=instance,
        )

@receiver(
    post_save,
    sender=ProjectMember,
)
def project_member_notification(
    sender,
    instance,
    created,
    **kwargs,
):

    if created:

        NotificationService.send_project_member_notification(
            instance,
        )


@receiver(
    pre_save,
    sender=Issue,
)
def cache_old_issue(
    sender,
    instance,
    **kwargs,
):

    if not instance.pk:

        return

    try:

        old = Issue.objects.get(
            pk=instance.pk,
        )

        instance._old_status = old.status

        instance._old_assignee = old.assignee

    except Issue.DoesNotExist:

        pass

@receiver(
    post_save,
    sender=Issue,
)
def assignment_notification(
    sender,
    instance,
    created,
    **kwargs,
):

    if created:

        NotificationService.send_issue_assignment_notification(
            instance,
        )

        return

    old_assignee = getattr(
        instance,
        "_old_assignee",
        None,
    )

    if old_assignee != instance.assignee:

        NotificationService.send_issue_assignment_notification(
            instance,
        )

@receiver(
    post_save,
    sender=Issue,
)
def status_notification(
    sender,
    instance,
    created,
    **kwargs,
):

    if created:

        return

    old_status = getattr(
        instance,
        "_old_status",
        None,
    )

    if old_status != instance.status:

        NotificationService.send_status_notification(

            issue=instance,

            old_status=old_status,

        )

@receiver(
    post_save,
    sender=Issue,
)
def completed_notification(
    sender,
    instance,
    created,
    **kwargs,
):

    if created:

        return

    if instance.status == Issue.Status.COMPLETED:

        NotificationService.notify_with_email(

            recipient=instance.reporter,

            title="Issue Completed",

            message=(
                f"Issue '{instance.title}' "
                "has been completed."
            ),

            notification_type="ISSUE",

        )


from django.contrib.auth.signals import (
    user_logged_in,
)


@receiver(
    user_logged_in,
)
def login_notification(
    sender,
    request,
    user,
    **kwargs,
):

    NotificationService.create_notification(

        recipient=user,

        title="Login Successful",

        message="You have logged in.",

        notification_type="SYSTEM",

    )

