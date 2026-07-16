from django import forms

from accounts.models import User

from .models import (
    Project,
    ProjectMember,
)


class ProjectCreateForm(forms.ModelForm):

    class Meta:

        model = Project

        fields = (
            "name",
            "description",
            "status",
            "start_date",
            "end_date",
        )

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Project Name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

    def clean_name(self):

        name = self.cleaned_data["name"]

        if len(name) < 3:

            raise forms.ValidationError(
                "Project name is too short."
            )

        return name

    def clean(self):

        cleaned_data = super().clean()

        start_date = cleaned_data.get(
            "start_date"
        )

        end_date = cleaned_data.get(
            "end_date"
        )

        if (
            start_date
            and end_date
            and start_date > end_date
        ):

            raise forms.ValidationError(
                "End date must be greater than start date."
            )

        return cleaned_data


class ProjectUpdateForm(forms.ModelForm):

    class Meta:

        model = Project

        fields = (
            "name",
            "description",
            "status",
            "start_date",
            "end_date",
        )

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        start_date = cleaned_data.get(
            "start_date"
        )

        end_date = cleaned_data.get(
            "end_date"
        )

        if (
            start_date
            and end_date
            and start_date > end_date
        ):

            raise forms.ValidationError(
                "End date must be greater than start date."
            )

        return cleaned_data


class ProjectMemberForm(forms.ModelForm):

    class Meta:

        model = ProjectMember

        fields = (
            "user",
            "role",
            "is_active",
        )

        widgets = {

            "user": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(
            self,
            *args,
            **kwargs
    ):
        super().__init__(
            *args,
            **kwargs
        )

        self.fields["user"].queryset = User.objects.filter(
            is_active=True
        )

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")

        project = self.instance.project if self.instance.pk else None

        if user and project and ProjectMember.objects.filter(
            project=project,
            user=user
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "This user is already a member of the project."
            )
        
        return cleaned_data
    
