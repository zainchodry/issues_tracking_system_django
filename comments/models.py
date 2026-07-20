from django.conf import settings
from django.db import models

from issues.models import Issue


class Comment(models.Model):

    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    message = models.TextField()

    is_edited = models.BooleanField(
        default=False,
    )

    is_deleted = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "created_at",
        ]

    def __str__(self):

        return f"{self.user.username} - {self.issue.title}"

    @property
    def has_replies(self):

        return self.replies.exists()

    @property
    def total_replies(self):

        return self.replies.count()

import os


def comment_attachment_path(
    instance,
    filename,
):

    return os.path.join(
        "comments",
        str(instance.comment.id),
        filename,
    )


class CommentAttachment(models.Model):

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    file = models.FileField(
        upload_to=comment_attachment_path,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):

        return os.path.basename(
            self.file.name,
        )
    
class CommentReaction(models.Model):

    class Reaction(models.TextChoices):

        LIKE = "LIKE", "Like"

        LOVE = "LOVE", "Love"

        LAUGH = "LAUGH", "Laugh"

        WOW = "WOW", "Wow"

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="reactions",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    reaction = models.CharField(
        max_length=20,
        choices=Reaction.choices,
        default=Reaction.LIKE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        unique_together = (
            "comment",
            "user",
        )

    def __str__(self):

        return f"{self.user.username} - {self.reaction}"
    
