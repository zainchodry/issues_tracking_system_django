from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Project(models.Model):

    class Status(models.TextChoices):
        PLANNING = "PLANNING", "Planning"
        ACTIVE = "ACTIVE", "Active"
        ON_HOLD = "ON_HOLD", "On Hold"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    name = models.CharField(
        max_length=150,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNING
    )

    start_date = models.DateField(
        blank=True,
        null=True
    )

    end_date = models.DateField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ProjectMember",
        related_name="projects",
        blank=True
    )

    class Meta:
        ordering = [
            "-created_at"
        ]

        verbose_name = "Project"

        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name

    def clean(self):

        if (
            self.start_date
            and self.end_date
            and self.start_date > self.end_date
        ):

            raise ValidationError(
                "End date must be greater than start date."
            )

    def save(
        self,
        *args,
        **kwargs
    ):

        if not self.slug:

            self.slug = slugify(self.name)

        self.full_clean()

        super().save(
            *args,
            **kwargs
        )

    @property
    def total_members(self):

        return self.project_members.count()

    @property
    def total_issues(self):

        return self.issues.count()

    @property
    def completed_issues(self):

        return self.issues.filter(
            status="COMPLETED"
        ).count()

    @property
    def pending_issues(self):

        return self.issues.filter(
            status="TODO"
        ).count()

    @property
    def progress(self):

        total = self.total_issues

        if total == 0:
            return 0

        return int(
            (
                self.completed_issues
                / total
            ) * 100
        )

    def get_absolute_url(self):

        return reverse(
            "projects:detail",
            kwargs={
                "slug": self.slug
            }
        )


class ProjectMember(models.Model):

    class Role(models.TextChoices):
        MANAGER = "MANAGER", "Manager"
        DEVELOPER = "DEVELOPER", "Developer"
        TESTER = "TESTER", "Tester"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_members"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_memberships"
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DEVELOPER
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:

        ordering = [
            "project",
            "user"
        ]

        unique_together = (
            "project",
            "user"
        )

        verbose_name = "Project Member"

        verbose_name_plural = "Project Members"

    def __str__(self):

        return f"{self.user.email} - {self.project.name}"