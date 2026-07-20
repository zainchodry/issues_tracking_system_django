from django import forms
from .models import *

class NotificationPreferenceForm(forms.ModelForm):

    class Meta:

        model = NotificationPreference

        fields = (

            "email_notifications",

            "browser_notifications",

            "issue_assignment",

            "issue_updates",

            "project_updates",

            "comment_notifications",

        )

        widgets = {

            "email_notifications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "browser_notifications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "issue_assignment": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "issue_updates": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "project_updates": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "comment_notifications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

class NotificationSearchForm(forms.Form):

    search = forms.CharField(

        required=False,

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "Search notifications",

            }

        ),

    )

    is_read = forms.ChoiceField(

        required=False,

        choices=(

            ("", "All"),

            ("True", "Read"),

            ("False", "Unread"),

        ),

        widget=forms.Select(

            attrs={

                "class": "form-select",

            }

        ),

    )

    notification_type = forms.ChoiceField(

        required=False,

        choices=[("", "All Types")] + list(
            Notification.NotificationType.choices
        ),

        widget=forms.Select(

            attrs={

                "class": "form-select",

            }

        ),

    )

