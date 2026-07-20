from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views import View

from .forms import (
    NotificationPreferenceForm,
)

from .models import (
    Notification,
    NotificationPreference,
)

from .services import (
    NotificationService,
)

class NotificationListView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
    ):

        notifications = (

            Notification.objects

            .filter(
                recipient=request.user,
            )

            .order_by(
                "-created_at",
            )

        )

        search = request.GET.get(
            "search",
        )

        is_read = request.GET.get(
            "is_read",
        )

        notification_type = request.GET.get(
            "notification_type",
        )

        if search:

            notifications = notifications.filter(

                Q(title__icontains=search)

                |

                Q(message__icontains=search)

            )

        if is_read == "True":

            notifications = notifications.filter(
                is_read=True,
            )

        elif is_read == "False":

            notifications = notifications.filter(
                is_read=False,
            )

        if notification_type:

            notifications = notifications.filter(
                notification_type=notification_type,
            )

        paginator = Paginator(
            notifications,
            15,
        )

        page_number = request.GET.get(
            "page",
        )

        page_obj = paginator.get_page(
            page_number,
        )

        context = {

            "notifications": page_obj,

        }

        return render(

            request,

            "notifications/notification_list.html",

            context,

        )
    
class NotificationDetailView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        pk,
    ):

        notification = get_object_or_404(

            Notification,

            pk=pk,

            recipient=request.user,

        )

        if not notification.is_read:

            NotificationService.mark_as_read(
                notification,
            )

        context = {

            "notification": notification,

        }

        return render(

            request,

            "notifications/notification_detail.html",

            context,

        )
    
class MarkNotificationReadView(
    LoginRequiredMixin,
    View,
):

    def post(
        self,
        request,
        pk,
    ):

        notification = get_object_or_404(

            Notification,

            pk=pk,

            recipient=request.user,

        )

        NotificationService.mark_as_read(
            notification,
        )

        messages.success(

            request,

            "Notification marked as read.",

        )

        return redirect(
            "notifications:list",
        )
    
class MarkNotificationUnreadView(
    LoginRequiredMixin,
    View,
):

    def post(
        self,
        request,
        pk,
    ):

        notification = get_object_or_404(

            Notification,

            pk=pk,

            recipient=request.user,

        )

        notification.is_read = False

        notification.read_at = None

        notification.save()

        messages.success(

            request,

            "Notification marked as unread.",

        )

        return redirect(
            "notifications:list",
        )
    
class MarkAllNotificationsReadView(
    LoginRequiredMixin,
    View,
):

    def post(
        self,
        request,
    ):

        NotificationService.mark_all_as_read(
            request.user,
        )

        messages.success(

            request,

            "All notifications marked as read.",

        )

        return redirect(
            "notifications:list",
        )
    
class DeleteNotificationView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        pk,
    ):

        notification = get_object_or_404(

            Notification,

            pk=pk,

            recipient=request.user,

        )

        context = {

            "notification": notification,

        }

        return render(

            request,

            "notifications/notification_confirm_delete.html",

            context,

        )

    def post(
        self,
        request,
        pk,
    ):

        notification = get_object_or_404(

            Notification,

            pk=pk,

            recipient=request.user,

        )

        NotificationService.delete_notification(
            notification,
        )

        messages.success(

            request,

            "Notification deleted successfully.",

        )

        return redirect(
            "notifications:list",
        )
    
class NotificationPreferenceUpdateView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
    ):

        preference, created = (
            NotificationPreference.objects.get_or_create(
                user=request.user,
            )
        )

        form = NotificationPreferenceForm(
            instance=preference,
        )

        context = {

            "form": form,

            "title": "Notification Preferences",

        }

        return render(

            request,

            "notifications/preferences.html",

            context,

        )

    def post(
        self,
        request,
    ):

        preference, created = (
            NotificationPreference.objects.get_or_create(
                user=request.user,
            )
        )

        form = NotificationPreferenceForm(

            request.POST,

            instance=preference,

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Preferences updated successfully.",

            )

            return redirect(
                "notifications:preferences",
            )

        context = {

            "form": form,

            "title": "Notification Preferences",

        }

        return render(

            request,

            "notifications/preferences.html",

            context,

        )
    
