from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

import accountapp
# from accountapp.models import User

#댓글알림
class Notification(models.Model):
    #1 = TeamComment, 2 = NewContest
    TYPE_CHOICES = (
        #(0, 'Announcement'),
        (1, 'TeamComment'),
        (2, 'NewContest'),

    )
    notification_type = models.IntegerField(choices=TYPE_CHOICES)
    to_user = models.ForeignKey('accountapp.User', related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey('accountapp.User', related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('teamapp.Team', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    # comment = models.ForeignKey('commentapp.TeamComment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
    text_preview = models.CharField(max_length=90, blank=True, null=True)
    #announcement = models.TextField(blank=True, null=True)
    #announcement_link = models.CharField(max_length=200, blank=True, null=True, default="/")

#대회공모전알림
class ContestNotification(models.Model):
    to_user = models.ForeignKey('accountapp.User', related_name='contest_notify', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)

#전체공지
class AnnouncementField(models.Model): # 관리자 작성창에서 AdminNotification으로 전달해 모든유저에게 돌릴것.
    date = models.DateTimeField(default=timezone.now)
    announcement_admin = models.TextField(blank=False, null=True)
    announcement_link = models.CharField(max_length=200, blank=True, null=True, default="/")

    def announcement(instance, *args, **kwargs):
        from accountapp.models import User
        Notification = instance
        announcement = Notification.announcement_admin
        announcement_link = Notification.announcement_link
        for user in User.objects.all():
            to_user = user
            notify = AdminNotification(to_user=to_user, announcement=announcement, announcement_link=announcement_link)
            notify.save()

class AdminNotification(models.Model):
    to_user = models.ForeignKey('accountapp.User', related_name='announcement_to', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
    announcement = models.TextField(blank=False, null=True)
    announcement_link = models.CharField(max_length=200, blank=True, null=True, default="/")


post_save.connect(AnnouncementField.announcement, sender=AnnouncementField)


