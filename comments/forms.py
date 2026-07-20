from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a comment...',
            }),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 2:
            raise forms.ValidationError('Comment must be at least 2 characters.')
        return message


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 2:
            raise forms.ValidationError('Comment must be at least 2 characters.')
        return message
