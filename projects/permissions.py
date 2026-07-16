from django.contrib import messages
from django.shortcuts import redirect

from accounts.models import User


def is_admin(user):

    return user.role == User.Roles.ADMIN


def is_manager(user):

    return user.role == User.Roles.MANAGER


def is_developer(user):

    return user.role == User.Roles.DEVELOPER


def can_manage_project(
    request,
    project,
):

    if is_admin(request.user):

        return True

    if project.owner == request.user:

        return True

    messages.error(
        request,
        "Permission denied.",
    )

    return False