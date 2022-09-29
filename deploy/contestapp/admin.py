from django.contrib import admin

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin

from contestapp.models import Contest


class ContestAdmin(SummernoteModelAdmin):
    summernote_fields = 'content'
    list_display = ['title','host','category']
    list_filter = ['category']
    search_fields = ['title', 'host']

    class Media:
        css = {
            'all': ('css/admin/team.css', )
        }

admin.site.register(Contest, ContestAdmin)