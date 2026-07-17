from django.contrib import admin

from .models import (
    Issue,
    IssueAttachment,
    IssueHistory,
)

class IssueAttachmentInline(admin.TabularInline):

    model = IssueAttachment

    extra = 0

    readonly_fields = (
        "uploaded_by",
        "uploaded_at",
    )

    fields = (
        "file",
        "uploaded_by",
        "uploaded_at",
    )

    autocomplete_fields = (
        "uploaded_by",
    )

class IssueHistoryInline(admin.TabularInline):

    model = IssueHistory

    extra = 0

    can_delete = False

    readonly_fields = (

        "action",

        "performed_by",

        "old_value",

        "new_value",

        "description",

        "created_at",

    )

    fields = (

        "action",

        "performed_by",

        "old_value",

        "new_value",

        "description",

        "created_at",

    )

    ordering = (
        "-created_at",
    )

    def has_add_permission(
        self,
        request,
        obj=None,
    ):
        return False

    def has_change_permission(
        self,
        request,
        obj=None,
    ):
        return False
    
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "title",

        "project",

        "reporter",

        "assignee",

        "issue_type",

        "priority",

        "status",

        "due_date",

        "created_at",

    )

    list_display_links = (

        "id",

        "title",

    )

    search_fields = (

        "title",

        "description",

        "project__name",

        "reporter__username",

        "assignee__username",

    )

    list_filter = (

        "status",

        "priority",

        "issue_type",

        "project",

        "created_at",

    )

    autocomplete_fields = (

        "project",

        "reporter",

        "assignee",

    )

    readonly_fields = (

        "created_at",

        "updated_at",

    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    inlines = [

        IssueAttachmentInline,

        IssueHistoryInline,

    ]

    fieldsets = (

        (

            "Issue Information",

            {

                "fields": (

                    "project",

                    "reporter",

                    "assignee",

                    "title",

                    "description",

                )

            },

        ),

        (

            "Tracking",

            {

                "fields": (

                    "issue_type",

                    "priority",

                    "status",

                    "estimated_hours",

                    "logged_hours",

                    "due_date",

                )

            },

        ),

        (

            "System",

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
        request,
    ):

        return (

            super()

            .get_queryset(request)

            .select_related(

                "project",

                "reporter",

                "assignee",

            )

        )
    
@admin.register(IssueAttachment)
class IssueAttachmentAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "issue",

        "uploaded_by",

        "uploaded_at",

    )

    search_fields = (

        "issue__title",

        "uploaded_by__username",

    )

    list_filter = (

        "uploaded_at",

    )

    autocomplete_fields = (

        "issue",

        "uploaded_by",

    )

    readonly_fields = (
        "uploaded_at",
    )

    ordering = (
        "-uploaded_at",
    )

@admin.register(IssueHistory)
class IssueHistoryAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "issue",

        "action",

        "performed_by",

        "created_at",

    )

    search_fields = (

        "issue__title",

        "performed_by__username",

    )

    list_filter = (

        "action",

        "created_at",

    )

    autocomplete_fields = (

        "issue",

        "performed_by",

    )

    readonly_fields = (

        "issue",

        "action",

        "performed_by",

        "old_value",

        "new_value",

        "description",

        "created_at",

    )

    ordering = (
        "-created_at",
    )

    def has_add_permission(
        self,
        request,
    ):
        return False

    def has_change_permission(
        self,
        request,
        obj=None,
    ):
        return False

    def has_delete_permission(
        self,
        request,
        obj=None,
    ):
        return False
    
