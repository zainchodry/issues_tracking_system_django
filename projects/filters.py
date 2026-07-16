from django.db.models import Q


class ProjectFilter:

    def __init__(
        self,
        request,
        queryset,
    ):

        self.request = request

        self.queryset = queryset

    def filter(self):

        search = self.request.GET.get(
            "search"
        )

        status = self.request.GET.get(
            "status"
        )

        owner = self.request.GET.get(
            "owner"
        )

        if search:

            self.queryset = self.queryset.filter(

                Q(name__icontains=search)

                |

                Q(description__icontains=search)

            )

        if status:

            self.queryset = self.queryset.filter(
                status=status
            )

        if owner:

            self.queryset = self.queryset.filter(
                owner__id=owner
            )

        return self.queryset
    