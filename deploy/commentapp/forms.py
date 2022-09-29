from django.forms import ModelForm, CharField, Textarea
from markdownx.fields import MarkdownxFormField

from commentapp.models import TeamComment, ContestComment


class TeamCommentCreationForm(ModelForm):
    class Meta:
        model = TeamComment
        fields = ['content']

class ContestCommentCreationForm(ModelForm):
    class Meta:
        model = ContestComment
        fields = ['content']