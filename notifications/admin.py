from django.contrib import admin
from django.utils import timezone

from .models import (
    Notification,
    NotificationPreference,
    EmailLog,
)

@admin.action(description="Mark selected notifications as read")
def mark_as_read(
    modeladmin,
    request,
    queryset,
):

    queryset.update(
        is_read=True,
        read_at=timezone.now(),
    )


@admin.action(description="Mark selected notifications as unread")
def mark_as_unread(
    modeladmin,
    request,
    queryset,
):

    queryset.update(
        is_read=False,
        read_at=None,
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "recipient",

        "title",

        "notification_type",

        "is_read",

        "created_at",

    )

    list_display_links = (

        "id",

        "title",

    )

    search_fields = (

        "title",

        "message",

        "recipient__username",

        "recipient__email",

    )

    list_filter = (

        "notification_type",

        "is_read",

        "created_at",

    )

    autocomplete_fields = (

        "recipient",

    )

    readonly_fields = (

        "recipient",

        "title",

        "message",

        "notification_type",

        "created_at",

        "read_at",

    )

    ordering = (

        "-created_at",

    )

    list_per_page = 25

    actions = (

        mark_as_read,

        mark_as_unread,

    )

    fieldsets = (

        (

            "Notification",

            {

                "fields": (

                    "recipient",

                    "title",

                    "message",

                    "notification_type",

                )

            },

        ),

        (

            "Status",

            {

                "fields": (

                    "is_read",

                    "read_at",

                )

            },

        ),

        (

            "System",

            {

                "fields": (

                    "created_at",

                )

            },

        ),

    )

    def get_queryset(
        self,
        request,
    ):

        return (

            super()

            .get_queryset(request)

            .select_related("recipient")

        )
    
@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):

    list_display = (

        "user",

        "email_notifications",

        "browser_notifications",

        "issue_assignment",

        "issue_updates",

        "project_updates",

        "comment_notifications",

    )

    search_fields = (

        "user__username",

        "user__email",

    )

    autocomplete_fields = (

        "user",

    )

    list_filter = (

        "email_notifications",

        "browser_notifications",

    )

    ordering = (

        "user__username",

    )

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "recipient",

        "subject",

        "status",

        "sent_at",

        "created_at",

    )

    list_display_links = (

        "id",

        "subject",

    )

    search_fields = (

        "recipient__username",

        "recipient__email",

        "subject",

    )

    list_filter = (

        "status",

        "created_at",

        "sent_at",

    )

    autocomplete_fields = (

        "recipient",

    )

    readonly_fields = (

        "created_at",

        "sent_at",

    )

    ordering = (

        "-created_at",

    )

    list_per_page = 25

    def get_queryset(
        self,
        request,
    ):

        return (

            super()

            .get_queryset(request)

            .select_related("recipient")

        )
    
