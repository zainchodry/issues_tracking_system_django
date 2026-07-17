from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
import os
from projects.models import Project


class Issue(models.Model):

    class IssueType(models.TextChoices):
        BUG = "BUG", "Bug"
        TASK = "TASK", "Task"
        STORY = "STORY", "Story"
        EPIC = "EPIC", "Epic"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        TESTING = "TESTING", "Testing"
        COMPLETED = "COMPLETED", "Completed"
        CLOSED = "CLOSED", "Closed"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues",
    )

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reported_issues",
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
        null=True,
        blank=True,
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    issue_type = models.CharField(
        max_length=20,
        choices=IssueType.choices,
        default=IssueType.TASK,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )

    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    logged_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

        verbose_name = "Issue"

        verbose_name_plural = "Issues"

    def __str__(self):

        return f"#{self.pk} - {self.title}"

    def clean(self):

        if (
            self.logged_hours
            and
            self.estimated_hours
            and
            self.logged_hours > self.estimated_hours
        ):

            raise ValidationError(
                "Logged hours cannot exceed estimated hours."
            )

    def save(
        self,
        *args,
        **kwargs,
    ):

        self.full_clean()

        super().save(
            *args,
            **kwargs,
        )

    @property
    def is_completed(self):

        return self.status in [
            self.Status.COMPLETED,
            self.Status.CLOSED,
        ]

    @property
    def progress(self):

        if self.status == self.Status.TODO:
            return 0

        if self.status == self.Status.IN_PROGRESS:
            return 50

        if self.status == self.Status.TESTING:
            return 80

        if self.status == self.Status.COMPLETED:
            return 100

        if self.status == self.Status.CLOSED:
            return 100

        return 0

    @property
    def is_overdue(self):

        from django.utils import timezone

        if not self.due_date:
            return False

        return (
            self.due_date < timezone.now().date()
            and
            not self.is_completed
        )

    def get_absolute_url(self):

        return reverse(
            "issues:detail",
            kwargs={
                "pk": self.pk,
            },
        )
    
def issue_attachment_path(instance, filename):

    extension = filename.split(".")[-1]

    filename = (
        f"issue_{instance.issue.id}_"
        f"{instance.uploaded_by.id}.{extension}"
    )

    return os.path.join(
        "issues",
        str(instance.issue.id),
        filename,
    )


class IssueAttachment(models.Model):

    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    file = models.FileField(
        upload_to=issue_attachment_path,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_issue_files",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-uploaded_at",
        ]

        verbose_name = "Issue Attachment"

        verbose_name_plural = "Issue Attachments"

    def __str__(self):

        return os.path.basename(
            self.file.name,
        )

    @property
    def filename(self):

        return os.path.basename(
            self.file.name,
        )

    @property
    def extension(self):

        return self.file.name.split(".")[-1]
    
class IssueHistory(models.Model):

    class Action(models.TextChoices):

        CREATED = "CREATED", "Created"

        UPDATED = "UPDATED", "Updated"

        ASSIGNED = "ASSIGNED", "Assigned"

        STATUS_CHANGED = (
            "STATUS_CHANGED",
            "Status Changed",
        )

        PRIORITY_CHANGED = (
            "PRIORITY_CHANGED",
            "Priority Changed",
        )

        COMMENTED = (
            "COMMENTED",
            "Comment Added",
        )

        ATTACHMENT_ADDED = (
            "ATTACHMENT_ADDED",
            "Attachment Added",
        )

        CLOSED = "CLOSED", "Closed"

        REOPENED = "REOPENED", "Reopened"

    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="history",
    )

    action = models.CharField(
        max_length=50,
        choices=Action.choices,
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="issue_histories",
    )

    old_value = models.TextField(
        blank=True,
    )

    new_value = models.TextField(
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

        verbose_name = "Issue History"

        verbose_name_plural = "Issue Histories"

    def __str__(self):

        return (
            f"{self.issue.title} - "
            f"{self.get_action_display()}"
        )
