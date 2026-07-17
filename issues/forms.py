from django import forms

from .models import (
    Issue,
    IssueAttachment,
)

class IssueCreateForm(forms.ModelForm):

    class Meta:

        model = Issue

        fields = (
            "project",
            "title",
            "description",
            "issue_type",
            "priority",
            "status",
            "assignee",
            "estimated_hours",
            "due_date",
        )

        widgets = {

            "project": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Issue title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                }
            ),

            "issue_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "assignee": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "estimated_hours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.25",
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

    def clean_title(self):

        title = self.cleaned_data["title"]

        if len(title.strip()) < 5:

            raise forms.ValidationError(
                "Title must contain at least 5 characters."
            )

        return title

    def clean(self):

        cleaned_data = super().clean()

        estimated_hours = cleaned_data.get(
            "estimated_hours"
        )

        if (
            estimated_hours is not None
            and estimated_hours < 0
        ):

            raise forms.ValidationError(
                "Estimated hours cannot be negative."
            )

        return cleaned_data
    
class IssueUpdateForm(forms.ModelForm):

    class Meta:

        model = Issue

        fields = (
            "title",
            "description",
            "issue_type",
            "priority",
            "status",
            "assignee",
            "estimated_hours",
            "logged_hours",
            "due_date",
        )

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                }
            ),

            "issue_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "assignee": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "estimated_hours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.25",
                }
            ),

            "logged_hours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.25",
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        estimated = cleaned_data.get(
            "estimated_hours"
        )

        logged = cleaned_data.get(
            "logged_hours"
        )

        if (
            estimated is not None
            and logged is not None
            and logged > estimated
        ):

            raise forms.ValidationError(
                "Logged hours cannot exceed estimated hours."
            )

        return cleaned_data
    
class IssueAttachmentForm(forms.ModelForm):

    class Meta:

        model = IssueAttachment

        fields = (
            "file",
        )

        widgets = {

            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_file(self):

        file = self.cleaned_data["file"]

        if file.size > 10 * 1024 * 1024:

            raise forms.ValidationError(
                "Maximum file size is 10 MB."
            )

        return file
    
