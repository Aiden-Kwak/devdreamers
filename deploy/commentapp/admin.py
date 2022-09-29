from django.contrib import admin

# Register your models here.
from markdownx.admin import MarkdownxModelAdmin

from commentapp.models import TeamComment, ContestComment

admin.site.register(TeamComment, MarkdownxModelAdmin)
admin.site.register(ContestComment, MarkdownxModelAdmin)