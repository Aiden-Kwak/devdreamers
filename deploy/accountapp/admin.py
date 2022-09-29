from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from accountapp.models import Interest, Stack, Profile, Activity, Award, Intern, Language, Certificate, User, AdvertiseMail


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'school','email', 'is_superuser', 'is_admin', 'is_active']
    list_filter = ['school']
    search_fields = ['username','profile__nickname']

class ProfileAdmin(admin.ModelAdmin):

    list_display = ['nickname', 'get_school', 'get_username']
    list_filter = ['user__school']
    search_fields = ['nickname']

    def get_school(self, obj):
        return obj.user.get_school_display()

    def get_username(self, obj):
        return obj.user.username

    get_school.admin_order_field  = 'user'
    get_school.short_description = '학교'

    get_username.admin_order_field  = 'user'
    get_username.short_description = '아이디'

class AdvertiseMailAdmin(SummernoteModelAdmin):
    summernote_fields = 'mail'

admin.site.register(Interest)
admin.site.register(Stack)
admin.site.register(Activity)
admin.site.register(Award)
admin.site.register(Intern)
admin.site.register(Language)
admin.site.register(Certificate)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(AdvertiseMail, AdvertiseMailAdmin)

# Register your models here.
