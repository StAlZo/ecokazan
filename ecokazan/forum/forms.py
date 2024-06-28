from django import forms

from .models import Comment


class CommentForm(forms.Form):

    content = forms.CharField(
        label="",
        widget=forms.Textarea
    )
