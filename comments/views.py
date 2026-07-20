from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import JsonResponse

from issues.models import Issue
from .models import Comment, CommentReaction
from .forms import CommentForm, CommentEditForm


class CommentCreateView(LoginRequiredMixin, View):
    """Create a comment on an issue."""

    def post(self, request, issue_pk):
        issue = get_object_or_404(Issue, pk=issue_pk)
        form = CommentForm(request.POST)
        parent_id = request.POST.get('parent_id')

        if form.is_valid():
            comment = form.save(commit=False)
            comment.issue = issue
            comment.user = request.user

            if parent_id:
                try:
                    parent = Comment.objects.get(pk=parent_id, issue=issue)
                    comment.parent = parent
                except Comment.DoesNotExist:
                    pass

            comment.save()
            messages.success(request, 'Comment added successfully.')
        else:
            messages.error(request, 'Failed to add comment.')

        return redirect('issues:detail', pk=issue.pk)


class CommentUpdateView(LoginRequiredMixin, View):
    """Edit an existing comment."""

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.user != request.user and request.user.role != 'ADMIN':
            messages.error(request, 'You cannot edit this comment.')
            return redirect('issues:detail', pk=comment.issue.pk)

        form = CommentEditForm(instance=comment)
        context = {
            'form': form,
            'comment': comment,
            'issue': comment.issue,
        }
        return render(request, 'comments/comment_form.html', context)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.user != request.user and request.user.role != 'ADMIN':
            messages.error(request, 'You cannot edit this comment.')
            return redirect('issues:detail', pk=comment.issue.pk)

        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.is_edited = True
            comment.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect('issues:detail', pk=comment.issue.pk)

        context = {
            'form': form,
            'comment': comment,
            'issue': comment.issue,
        }
        return render(request, 'comments/comment_form.html', context)


class CommentDeleteView(LoginRequiredMixin, View):
    """Soft-delete a comment."""

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        issue_pk = comment.issue.pk

        if comment.user != request.user and request.user.role != 'ADMIN':
            messages.error(request, 'You cannot delete this comment.')
            return redirect('issues:detail', pk=issue_pk)

        comment.is_deleted = True
        comment.message = '[deleted]'
        comment.save(update_fields=['is_deleted', 'message'])
        messages.success(request, 'Comment deleted.')
        return redirect('issues:detail', pk=issue_pk)


class CommentReactionView(LoginRequiredMixin, View):
    """Toggle a reaction on a comment (AJAX-friendly)."""

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        reaction_type = request.POST.get('reaction', CommentReaction.Reaction.LIKE)

        existing = CommentReaction.objects.filter(comment=comment, user=request.user).first()
        if existing:
            if existing.reaction == reaction_type:
                existing.delete()
                reacted = False
            else:
                existing.reaction = reaction_type
                existing.save(update_fields=['reaction'])
                reacted = True
        else:
            CommentReaction.objects.create(
                comment=comment,
                user=request.user,
                reaction=reaction_type,
            )
            reacted = True

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'reacted': reacted,
                'count': comment.reactions.count(),
            })

        return redirect('issues:detail', pk=comment.issue.pk)
