import sys
from datetime import datetime, timedelta, timezone, date
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from multiselectfield import MultiSelectField

from accountapp.models import User
from notificationapp.models import ContestNotification

CONTEST_TYPES = (('SW창업', 'SW창업'),
                 ('웹/앱 개발', '웹/앱 개발'),
                 ('게임', '게임'),
                 ('보안', '보안'),
                 ('AI/빅데이터', 'AI/빅데이터'),
                 ('알고리즘', '알고리즘'),
                 ('임베디드', '임베디드'),
                 ('로봇/자율주행', '로봇/자율주행'),
                 ('AR/VR', 'AR/VR'),
                 ('기타', '기타'),
                )


class Contest(models.Model):  # crawled_data와 공유할것
    title = models.CharField(max_length=100, null=True, unique=True) # 공모전이름
    host = models.CharField(max_length=100, null=True) # 주최/주관
    participant = models.CharField(max_length=40, null=True) #공모대상
    homepage = models.URLField(blank=True) # 홈페이지 주소
    category = MultiSelectField(choices=CONTEST_TYPES, null=True) # 공모전분야
    start_date = models.DateField(null=True) #모집기간 시작일
    finish_date = models.DateField(null=True) #모집기간 마감일
    created_at = models.DateTimeField(auto_now_add=True, null=True) # 생성일
    image = models.ImageField(upload_to='contest/', null=True)  # 공모전 이미지
    content = models.TextField(blank=False, null=True,
                               default='<h4 class="content-title">⚙️대회명 |</h4><br>'
                                       '<h4 class="content-title">⚙️공모주제 |</h4><br>'
                                       '<h4 class="content-title">⚙️접수기간 및 일정 |</h4><br>'
                                       '<h4 class="content-title">⚙️참가대상 |</h4><br>'
                                       '<h4 class="content-title">⚙️시상내역 |</h4><br>'
                                       '<h4 class="content-title">⚙️참가방법 |</h4><br>'
                                       '<h4 class="content-title">⚙️기타사항 |</h4><br>'
                                       '<h4 class="content-title">⚙️주최/주관 |</h4><br>'
                                       '<h4 class="content-title">⚙️문의 |</h4><br>'
                                       '<h4 class="content-title">⚙️포스터 |</h4><br>') # 세부사항 글 작성

    visible = models.BooleanField(default=True)

    def save(self):
        image = Image.open(self.image)
        output = BytesIO()
        image = image.resize((265, 338))
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(output, format='JPEG', quality=99)
        output.seek(0)
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
        super(Contest, self).save()

    @property
    def show_deadline(self):
        time = self.finish_date - date.today()

        if time < timedelta(days=0):
            return '모집 마감', False
        # elif time < timedelta(minutes=1):
        #     return '잠시 후 마감', True
        # elif time < timedelta(hours=1):
        #     return str(int(time.seconds // 60)) + '분 후 마감', True
        # elif time < timedelta(hours=24):
        #     return str(int(time.seconds // 3600)) + '시간 후 마감', True
        elif time <= timedelta(days=7):
            return str(time.days) + '일 후 마감', True
        else:
            return str(time.days) + '일 후 마감', False

    def contest_add_notify(instance, *args, **kwargs):
        for user in User.objects.all():
            to_user = user
            notify = ContestNotification(to_user=to_user)
            notify.save()


post_save.connect(Contest.contest_add_notify, sender=Contest)

