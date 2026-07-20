from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.models import model_to_dict
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views import View

from .forms import (
    IssueCreateForm,
    IssueUpdateForm,
)

from .models import (
    Issue,
    IssueAttachment,
    IssueHistory,
)

from projects.models import (
    Project,
)


class IssueListView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
    ):

        issues = (
            Issue.objects
            .select_related(
                "project",
                "reporter",
                "assignee",
            )
            .order_by("-created_at")
        )

        search = request.GET.get("search")
        status = request.GET.get("status")
        priority = request.GET.get("priority")
        project = request.GET.get("project")

        if request.user.role == "DEVELOPER":
            issues = issues.filter(assignee=request.user)
        elif request.user.role == "MANAGER":
            issues = issues.filter(
                Q(reporter=request.user)
                | Q(assignee=request.user)
                | Q(project__owner=request.user)
            ).distinct()

        if search:
            issues = issues.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
            )

        if status:
            issues = issues.filter(status=status)

        if priority:
            issues = issues.filter(priority=priority)

        if project:
            issues = issues.filter(project_id=project)

        paginator = Paginator(issues, 10)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)

        projects_list = Project.objects.all()

        context = {
            "issues": page_obj,
            "search": search,
            "status": status,
            "priority": priority,
            "project": project,
            "projects_list": projects_list,
            "status_choices": Issue.Status.choices,
            "priority_choices": Issue.Priority.choices,
        }

        return render(request, "issues/issue_list.html", context)


class IssueDetailView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        pk,
    ):
        from comments.models import Comment
        from comments.forms import CommentForm

        issue = get_object_or_404(
            Issue.objects
            .select_related("project", "reporter", "assignee")
            .prefetch_related("attachments", "history", "comments"),
            pk=pk,
        )

        attachments = issue.attachments.all()
        history = issue.history.all()
        comments = issue.comments.filter(parent=None).select_related('user').prefetch_related(
            'replies__user', 'reactions'
        )
        comment_form = CommentForm()

        context = {
            "issue": issue,
            "attachments": attachments,
            "history": history,
            "comments": comments,
            "comment_form": comment_form,
        }

        return render(request, "issues/issue_detail.html", context)

class IssueCreateView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
    ):

        form = IssueCreateForm()

        return render(

            request,

            "issues/issue_form.html",

            {

                "form": form,

                "title": "Create Issue",

            },

        )

    def post(
        self,
        request,
    ):

        form = IssueCreateForm(

            request.POST,

        )

        if form.is_valid():

            issue = form.save(
                commit=False
            )

            issue.reporter = request.user

            issue.save()

            files = request.FILES.getlist(
                "files"
            )

            for file in files:

                IssueAttachment.objects.create(

                    issue=issue,

                    file=file,

                    uploaded_by=request.user,

                )

            IssueHistory.objects.create(

                issue=issue,

                action=IssueHistory.Action.CREATED,

                performed_by=request.user,

                description="Issue created.",

            )

            messages.success(

                request,

                "Issue created successfully.",

            )

            return redirect(

                "issues:detail",

                pk=issue.pk,

            )

        return render(

            request,

            "issues/issue_form.html",

            {

                "form": form,

                "title": "Create Issue",

            },

        )
    
class IssueUpdateView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        pk,
    ):

        issue = get_object_or_404(
            Issue,
            pk=pk,
        )

        form = IssueUpdateForm(
            instance=issue,
        )

        context = {

            "form": form,

            "issue": issue,

            "title": "Update Issue",

        }

        return render(

            request,

            "issues/issue_form.html",

            context,

        )

    def post(
        self,
        request,
        pk,
    ):

        issue = get_object_or_404(
            Issue,
            pk=pk,
        )

        previous = model_to_dict(
            issue,
        )

        form = IssueUpdateForm(

            request.POST,

            instance=issue,

        )

        if form.is_valid():

            issue = form.save()

            files = request.FILES.getlist(
                "files"
            )

            for file in files:

                IssueAttachment.objects.create(

                    issue=issue,

                    file=file,

                    uploaded_by=request.user,

                )

            current = model_to_dict(
                issue,
            )

            track_fields = [

                "status",

                "priority",

                "assignee",

                "title",

            ]

            for field in track_fields:

                old = previous.get(field)

                new = current.get(field)

                if old != new:

                    IssueHistory.objects.create(

                        issue=issue,

                        action=IssueHistory.Action.UPDATED,

                        performed_by=request.user,

                        old_value=str(old),

                        new_value=str(new),

                        description=f"{field} updated.",

                    )

            messages.success(

                request,

                "Issue updated successfully.",

            )

            return redirect(

                "issues:detail",

                pk=issue.pk,

            )

        context = {

            "form": form,

            "issue": issue,

            "title": "Update Issue",

        }

        return render(

            request,

            "issues/issue_form.html",

            context,

        )
    
class IssueDeleteView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        pk,
    ):

        issue = get_object_or_404(

            Issue,

            pk=pk,

        )

        return render(

            request,

            "issues/issue_confirm_delete.html",

            {

                "issue": issue,

            },

        )

    def post(
        self,
        request,
        pk,
    ):

        issue = get_object_or_404(

            Issue,

            pk=pk,

        )

        issue.delete()

        messages.success(

            request,

            "Issue deleted successfully.",

        )

        return redirect(
            "issues:list",
        )