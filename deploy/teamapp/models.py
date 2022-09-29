from datetime import datetime, timedelta, timezone

from django.db import models

# Create your models here.
from multiselectfield import MultiSelectField
from pytz import utc

from accountapp.models import User, Profile

DEV_CHOICES = (('서버/백엔드','서버/백엔드'),
              ('프론트엔드','프론트엔드'),
              ('DevOps','DevOps'),
              ('안드로이드 앱','안드로이드 앱'),
              ('아이폰 앱','아이폰 앱'),
              ('UI/UX', 'UI/UX'),
              ('데이터 엔지니어', '데이터 엔지니어'),
              ('머신러닝/AI', '머신러닝/AI'),
              ('게임 개발', '게임 개발'),
              ('AR/VR', 'AR/VR'),
              ('그래픽 디자인', '그래픽 디자인'),
              ('임베디드', '임베디드'),
              ('IoT', 'IoT'),
              ('보안', '보안'),
              ('블록체인', '블록체인'),
              ('알고리즘', '알고리즘'),
              ('기획/PM', '기획/PM'),
              ('마케팅', '마케팅'),
              ('기타', '기타'))

TEAM_CHOICES = (('0', '스터디'),
            ('1', '프로젝트'),
            ('2', '대회/공모전'),
            ('3', '동아리'),
            ('4', '스타트업/창업'),)

OPEN_CHOICES = ((False, '자신 학교에만 공개하기'), (True, '모든 학교에 공개하기'))

class Team(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team', null=True)

    title = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=45, null=True)
    type = models.CharField(max_length=2, choices=TEAM_CHOICES, default='0')
    category = MultiSelectField(choices=DEV_CHOICES, max_choices=3, null=True)

    content = models.TextField(blank=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    team_color = models.CharField(max_length=25, default='rgba(240, 116, 137, 1)')
    deadline = models.DateTimeField(null=True)
    contact = models.CharField(max_length=1024, blank=False)

    image = models.ImageField(upload_to='team/', default='../static/img/team-default.jpg')
    visible = models.BooleanField(default=True)

    to_open = models.BooleanField(default=True, choices=OPEN_CHOICES)


    def __str__(self):
        return self.title

    @property
    def show_date(self):
        time = datetime.now() - self.updated_at

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

    @property
    def show_deadline(self):
        time = self.deadline - datetime.now()

        if time.total_seconds() < 0:
            return '모집 마감', False
        elif time < timedelta(minutes=1):
            return '잠시 후 마감', True
        elif time < timedelta(hours=1):
            return str(int(time.seconds // 60)) + '분 후 마감', True
        elif time < timedelta(hours=24):
            return str(int(time.seconds // 3600)) + '시간 후 마감', True
        elif time <= timedelta(days=7):
            return str(time.days) + '일 후 마감', True
        else:
            return str(time.days) + '일 후 마감', False