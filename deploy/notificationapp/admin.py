from django.contrib import admin

# from notificationapp.models import Notifications
from notificationapp.models import Notification, AdminNotification, ContestNotification, AnnouncementField
from django_summernote.admin import SummernoteModelAdmin

class NotificationAdmin(SummernoteModelAdmin):
    summernote_fields = 'announcement_admin'

# class NotificationAdmin2(SummernoteModelAdmin):
#     summernote_fields = 'announcement'

admin.site.register(Notification)
admin.site.register(ContestNotification)
admin.site.register(AnnouncementField, NotificationAdmin) #어드민 공지작성창
# admin.site.register(AdminNotification, NotificationAdmin2) # 테스트후 필요없으니 삭제
