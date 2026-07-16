from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from accounts.models import User
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views import View
from projects.forms import *
from .forms import (
    ProjectCreateForm,
    ProjectUpdateForm,
)

from .models import (
    Project,
    ProjectMember,
)


class ProjectListView(
    LoginRequiredMixin,
    View
):

    def get(
        self,
        request,
    ):

        projects = (
            Project.objects
            .select_related("owner")
            .prefetch_related(
                "project_members"
            )
        )

        search = request.GET.get(
            "search"
        )

        status = request.GET.get(
            "status"
        )

        if request.user.role == "ADMIN":

            projects = projects

        elif request.user.role == "MANAGER":

            projects = projects.filter(

                Q(owner=request.user)

                |

                Q(
                    project_members__user=request.user
                )

            ).distinct()

        else:

            projects = projects.filter(

                project_members__user=request.user

            ).distinct()

        if search:

            projects = projects.filter(

                Q(name__icontains=search)

                |

                Q(description__icontains=search)

            )

        if status:

            projects = projects.filter(
                status=status
            )

        paginator = Paginator(
            projects,
            10,
        )

        page_number = request.GET.get(
            "page"
        )

        page_obj = paginator.get_page(
            page_number
        )

        context = {

            "projects": page_obj,

            "search": search,

            "status": status,

        }

        return render(

            request,

            "projects/project_list.html",

            context,

        )
    
class ProjectDetailView(
    LoginRequiredMixin,
    View
):

    def get(
        self,
        request,
        slug,
    ):

        project = get_object_or_404(

            Project.objects.select_related(
                "owner"
            ),

            slug=slug,

        )

        if (

            request.user.role != "ADMIN"

            and

            project.owner != request.user

            and

            not ProjectMember.objects.filter(

                project=project,

                user=request.user,

            ).exists()

        ):

            messages.error(

                request,

                "Permission denied."

            )

            return redirect(
                "projects:list"
            )

        members = (

            ProjectMember.objects

            .filter(
                project=project
            )

            .select_related(
                "user"
            )

        )

        issues = project.issues.all()

        context = {

            "project": project,

            "members": members,

            "issues": issues,

        }

        return render(

            request,

            "projects/project_detail.html",

            context,

        )
    
class ProjectCreateView(
    LoginRequiredMixin,
    View
):

    def get(
        self,
        request,
    ):

        if request.user.role == "DEVELOPER":

            messages.error(

                request,

                "Permission denied."

            )

            return redirect(
                "projects:list"
            )

        form = ProjectCreateForm()

        context = {

            "form": form,

            "title": "Create Project",

        }

        return render(

            request,

            "projects/project_form.html",

            context,

        )

    def post(
        self,
        request,
    ):

        if request.user.role == "DEVELOPER":

            messages.error(

                request,

                "Permission denied."

            )

            return redirect(
                "projects:list"
            )

        form = ProjectCreateForm(
            request.POST
        )

        if form.is_valid():

            project = form.save(
                commit=False
            )

            project.owner = request.user

            project.save()

            ProjectMember.objects.create(

                project=project,

                user=request.user,

                role="MANAGER",

            )

            messages.success(

                request,

                "Project created successfully."

            )

            return redirect(
                "projects:list"
            )

        context = {

            "form": form,

            "title": "Create Project",

        }

        return render(

            request,

            "projects/project_form.html",

            context,

        )
    
class ProjectUpdateView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        slug,
    ):

        project = get_object_or_404(
            Project,
            slug=slug,
        )

        if (
            request.user.role != "ADMIN"
            and project.owner != request.user
        ):

            messages.error(
                request,
                "You don't have permission to update this project.",
            )

            return redirect(
                "projects:list",
            )

        form = ProjectUpdateForm(
            instance=project,
        )

        context = {

            "form": form,

            "project": project,

            "title": "Update Project",

        }

        return render(
            request,
            "projects/project_form.html",
            context,
        )

    def post(
        self,
        request,
        slug,
    ):

        project = get_object_or_404(
            Project,
            slug=slug,
        )

        if (
            request.user.role != "ADMIN"
            and project.owner != request.user
        ):

            messages.error(
                request,
                "You don't have permission to update this project.",
            )

            return redirect(
                "projects:list",
            )

        form = ProjectUpdateForm(
            request.POST,
            instance=project,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Project updated successfully.",
            )

            return redirect(
                "projects:detail",
                slug=project.slug,
            )

        context = {

            "form": form,

            "project": project,

            "title": "Update Project",

        }

        return render(
            request,
            "projects/project_form.html",
            context,
        )
    
class ProjectDeleteView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        slug,
    ):

        project = get_object_or_404(
            Project,
            slug=slug,
        )

        if (
            request.user.role != "ADMIN"
            and project.owner != request.user
        ):

            messages.error(
                request,
                "You don't have permission to delete this project.",
            )

            return redirect(
                "projects:list",
            )

        context = {

            "project": project,

        }

        return render(
            request,
            "projects/project_confirm_delete.html",
            context,
        )

    def post(
        self,
        request,
        slug,
    ):

        project = get_object_or_404(
            Project,
            slug=slug,
        )

        if (
            request.user.role != "ADMIN"
            and project.owner != request.user
        ):

            messages.error(
                request,
                "You don't have permission to delete this project.",
            )

            return redirect(
                "projects:list",
            )

        project.delete()

        messages.success(
            request,
            "Project deleted successfully.",
        )

        return redirect(
            "projects:list",
        )
    
from accounts.models import User


class ProjectMemberListView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        slug,
    ):

        project = get_object_or_404(
            Project,
            slug=slug,
        )

        if (
            request.user.role != User.Roles.ADMIN
            and project.owner != request.user
        ):

            messages.error(
                request,
                "Permission denied.",
            )

            return redirect(
                "projects:list",
            )

        members = (
            ProjectMember.objects
            .filter(project=project)
            .select_related("user")
            .order_by("user__username")
        )

        context = {

            "project": project,

            "members": members,

        }

        return render(
            request,
            "projects/project_member_list.html",
            context,
        )


class ProjectMemberCreateView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        slug,
    ):

        project = get_object_or_404(
            Project,
            slug=slug,
        )

        form = ProjectMemberForm()

        context = {

            "project": project,

            "form": form,

            "title": "Add Member",

        }

        return render(
            request,
            "projects/project_member_form.html",
            context,
        )

    def post(
        self,
        request,
        slug,
    ):

        project = get_object_or_404(
            Project,
            slug=slug,
        )

        form = ProjectMemberForm(
            request.POST,
        )

        if form.is_valid():

            member = form.save(
                commit=False,
            )

            member.project = project

            if ProjectMember.objects.filter(
                project=project,
                user=member.user,
            ).exists():

                messages.error(
                    request,
                    "User already exists in this project.",
                )

                return redirect(
                    "projects:member-list",
                    slug=project.slug,
                )

            member.save()

            messages.success(
                request,
                "Member added successfully.",
            )

            return redirect(
                "projects:member-list",
                slug=project.slug,
            )

        context = {

            "project": project,

            "form": form,

            "title": "Add Member",

        }

        return render(
            request,
            "projects/project_member_form.html",
            context,
        )


class ProjectMemberUpdateView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        pk,
    ):

        member = get_object_or_404(
            ProjectMember,
            pk=pk,
        )

        form = ProjectMemberForm(
            instance=member,
        )

        context = {

            "member": member,

            "project": member.project,

            "form": form,

            "title": "Update Member",

        }

        return render(
            request,
            "projects/project_member_form.html",
            context,
        )

    def post(
        self,
        request,
        pk,
    ):

        member = get_object_or_404(
            ProjectMember,
            pk=pk,
        )

        form = ProjectMemberForm(
            request.POST,
            instance=member,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Member updated successfully.",
            )

            return redirect(
                "projects:member-list",
                slug=member.project.slug,
            )

        context = {

            "member": member,

            "project": member.project,

            "form": form,

            "title": "Update Member",

        }

        return render(
            request,
            "projects/project_member_form.html",
            context,
        )


class ProjectMemberDeleteView(
    LoginRequiredMixin,
    View,
):

    def post(
        self,
        request,
        pk,
    ):

        member = get_object_or_404(
            ProjectMember,
            pk=pk,
        )

        project_slug = member.project.slug

        if member.project.owner != request.user and (
            request.user.role != User.Roles.ADMIN
        ):

            messages.error(
                request,
                "Permission denied.",
            )

            return redirect(
                "projects:list",
            )

        member.delete()

        messages.success(
            request,
            "Member removed successfully.",
        )

        return redirect(
            "projects:member-list",
            slug=project_slug,
        )