from django.contrib import admin

from .models import (
    Project,
    ProjectMember,
)


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1
    autocomplete_fields = (
        "user",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "owner",
        "status",
        "start_date",
        "end_date",
        "created_at",
    )

    list_display_links = (
        "id",
        "name",
    )

    list_filter = (
        "status",
        "created_at",
        "start_date",
        "end_date",
    )

    search_fields = (
        "name",
        "description",
        "owner__email",
        "owner__username",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "slug",
    )

    prepopulated_fields = {
        "slug": (
            "name",
        )
    }

    autocomplete_fields = (
        "owner",
    )

    inlines = [
        ProjectMemberInline,
    ]

    fieldsets = (

        (
            "Project Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                )
            },
        ),

        (
            "Management",
            {
                "fields": (
                    "owner",
                    "status",
                )
            },
        ),

        (
            "Timeline",
            {
                "fields": (
                    "start_date",
                    "end_date",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def get_queryset(
        self,
        request
    ):

        queryset = super().get_queryset(request)

        return queryset.select_related(
            "owner"
        )


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "project",
        "user",
        "role",
        "is_active",
        "joined_at",
    )

    list_display_links = (
        "id",
        "project",
    )

    search_fields = (
        "project__name",
        "user__email",
        "user__username",
    )

    list_filter = (
        "role",
        "is_active",
        "joined_at",
    )

    ordering = (
        "-joined_at",
    )

    autocomplete_fields = (
        "project",
        "user",
    )

    readonly_fields = (
        "joined_at",
    )

    fieldsets = (

        (
            "Project Member",
            {
                "fields": (
                    "project",
                    "user",
                    "role",
                    "is_active",
                )
            },
        ),

        (
            "Dates",
            {
                "fields": (
                    "joined_at",
                )
            },
        ),
    )

    def get_queryset(
        self,
        request
    ):

        queryset = super().get_queryset(request)

        return queryset.select_related(
            "project",
            "user",
        )