from datetime import datetime, timedelta

from django.db import models
from datetime import datetime, timedelta, timezone

# Create your models here.
from django.db.models.signals import post_save
from markdown import markdown

from accountapp.models import User
from contestapp.models import Contest
from notificationapp.models import Notification
from teamapp.models import Team

# from notificationapp.models import Notifications


class TeamComment(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comment')

    content = models.TextField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now=True)

    def get_content_markdown(self):
        return markdown(self.content)

    @property
    def show_date(self):
        time = datetime.now() - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds // 60)) + '분 전'
        elif time < timedelta(hours=24):
            return str(int(time.seconds // 3600)) + '시간 전'
        elif time < timedelta(days=7):
            return str(time.days) + '일 전'
        else:
            return str(time.days // 7) + '주 전'

    def team_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.team
        sender = comment.user
        receive = comment.team.writer
        text_preview = comment.content[:50]
        if sender == receive:
            pass
        else:
            notify = Notification(post=post, from_user=sender, to_user=receive, text_preview=text_preview, notification_type=1)
            notify.save()


class ContestComment(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, null=True, related_name='contest_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='contest_comment')

    content = models.TextField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now=True)

    def get_content_markdown(self):
        return markdown(self.content)

    @property
    def show_date(self):
        time = datetime.now() - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds // 60)) + '분 전'
        elif time < timedelta(hours=24):
            return str(int(time.seconds // 3600)) + '시간 전'
        elif time < timedelta(days=7):
            return str(time.days) + '일 전'
        else:
            return str(time.days // 7) + '주 전'


#Comment Signal stuff
post_save.connect(TeamComment.team_comment_post, sender=TeamComment)