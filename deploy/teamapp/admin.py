from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Team
# Register your models here.

class TeamAdmin(SummernoteModelAdmin):
    summernote_fields = 'content'
    list_display = ['title','get_username','get_nickname']
    list_filter = ['category']
    search_fields = ['title', 'writer__profile__nickname', 'writer__username']

    def get_nickname(self, obj):
        return obj.writer.profile.nickname

    def get_username(self, obj):
        return obj.writer.username

    get_nickname.admin_order_field  = 'writer'
    get_nickname.short_description = '닉네임'

    get_username.admin_order_field = 'writer'
    get_username.short_description = '아이디'

    class Media:
        css = {
            'all': ('css/admin/team.css', )
        }

admin.site.register(Team, TeamAdmin)