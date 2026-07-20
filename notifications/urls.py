from django.urls import path

from .views import (
    NotificationListView,
    NotificationDetailView,
    MarkNotificationReadView,
    MarkNotificationUnreadView,
    MarkAllNotificationsReadView,
    DeleteNotificationView,
    NotificationPreferenceUpdateView,
)

app_name = "notifications"

urlpatterns = [

    path(
        "",
        NotificationListView.as_view(),
        name="list",
    ),

    path(
        "<int:pk>/",
        NotificationDetailView.as_view(),
        name="detail",
    ),

    path(
        "<int:pk>/read/",
        MarkNotificationReadView.as_view(),
        name="read",
    ),

    path(
        "<int:pk>/unread/",
        MarkNotificationUnreadView.as_view(),
        name="unread",
    ),

    path(
        "read-all/",
        MarkAllNotificationsReadView.as_view(),
        name="read-all",
    ),

    path(
        "<int:pk>/delete/",
        DeleteNotificationView.as_view(),
        name="delete",
    ),

    path(
        "preferences/",
        NotificationPreferenceUpdateView.as_view(),
        name="preferences",
    ),

]