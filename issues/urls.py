from django.urls import path

from .views import (
    IssueListView,
    IssueDetailView,
    IssueCreateView,
    IssueUpdateView,
    IssueDeleteView,
)

app_name = "issues"

urlpatterns = [

    # ==========================
    # Issues
    # ==========================

    path(
        "",
        IssueListView.as_view(),
        name="list",
    ),

    path(
        "create/",
        IssueCreateView.as_view(),
        name="create",
    ),

    path(
        "<int:pk>/",
        IssueDetailView.as_view(),
        name="detail",
    ),

    path(
        "<int:pk>/update/",
        IssueUpdateView.as_view(),
        name="update",
    ),

    path(
        "<int:pk>/delete/",
        IssueDeleteView.as_view(),
        name="delete",
    ),

]