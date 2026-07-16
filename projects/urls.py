from django.urls import path

from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectMemberListView,
    ProjectMemberCreateView,
    ProjectMemberUpdateView,
    ProjectMemberDeleteView,
)

app_name = "projects"

urlpatterns = [

    # ==========================
    # Project URLs
    # ==========================

    path(
        "",
        ProjectListView.as_view(),
        name="list",
    ),

    path(
        "create/",
        ProjectCreateView.as_view(),
        name="create",
    ),

    path(
        "<slug:slug>/",
        ProjectDetailView.as_view(),
        name="detail",
    ),

    path(
        "<slug:slug>/update/",
        ProjectUpdateView.as_view(),
        name="update",
    ),

    path(
        "<slug:slug>/delete/",
        ProjectDeleteView.as_view(),
        name="delete",
    ),

    # ==========================
    # Project Members
    # ==========================

    path(
        "<slug:slug>/members/",
        ProjectMemberListView.as_view(),
        name="member-list",
    ),

    path(
        "<slug:slug>/members/add/",
        ProjectMemberCreateView.as_view(),
        name="member-add",
    ),

    path(
        "members/<int:pk>/update/",
        ProjectMemberUpdateView.as_view(),
        name="member-update",
    ),

    path(
        "members/<int:pk>/delete/",
        ProjectMemberDeleteView.as_view(),
        name="member-delete",
    ),

]