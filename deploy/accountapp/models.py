from datetime import datetime, timedelta, timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.db.models.signals import post_save
from django.utils import timezone

from notificationapp.models import AdminNotification


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None):
        if not username:
            raise ValueError('must have user username!')
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        superuser = self.create_user(
            username=username,
            email=email,
            password=password
        )
        superuser.is_admin = True
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save()
        return superuser


class User(AbstractBaseUser):
    STATUS_CHOICES = (
        ('0', '재학'),
        ('1', '휴학'),
        ('2', '졸업예정'),
        ('3', '졸업')
    )

    SCHOOL_CHOICES = (
        ('0','성균관대학교'),
        ('1','광주과학기술원'),
        ('2','서강대학교'),
        ('3','울산과학기술원'),
        ('4','중앙대학교'),
        ('5','한국과학기술원'),
        ('6','한양대학교'),
        ('7','서울대학교'),
        ('8','연세대학교'),
        ('9','고려대학교'),
        ('10','경희대학교'),
        ('11','한국외국어대학교'),
        ('12','서울시립대학교'),
        ('13','가톨릭대학교'),
        ('14','건국대학교'),
        ('15','광운대학교'),
        ('16','국민대학교'),
        ('17','동국대학교'),
        ('18','서울과학기술대학교'),
        ('19','세종대학교'),
        ('20','숭실대학교'),
        ('21','홍익대학교'),
        ('22','가천대학교'),
        ('23','인하대학교'),
        ('24','아주대학교'),
        ('25','한국항공대학교'),
        ('26','이화여자대학교'),
        ('27','성신여자대학교'),
        ('28','서울여자대학교'),
        ('29','숙명여자대학교'),
        ('30','동덕여자대학교'),
        ('31','덕성여자대학교'),
        ('32','한국예술종합학교'),
        ('33','대구경북과학기술원'),
        ('34','포항공과대학교'),
        ('35','전남대학교'),
        ('36','한동대학교'),
        ('37','충남대학교'),
        ('38','부산대학교'),
        ('39', '베를린 자유 대학교'),
    )

    username_pattern = RegexValidator(r'^[0-9a-zA-Z_]{5,20}$', '5-20글자 사이의 숫자,영문,언더바만 가능합니다!')
    objects = UserManager()

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=20, null=False,
                                unique=True, validators=[username_pattern])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    school = models.CharField(choices=SCHOOL_CHOICES, max_length=2, null=True)
    department = models.CharField(max_length=20, null=True)
    school_status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='0')
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def show_date(self):
        time = datetime.now() - self.last_login

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
    def show_since_date(self):
        diff = datetime.now() - self.date_joined
        return diff.days
    
    @property
    def since_date_event(self):
        if self.show_since_date == 0:
            return 0
        elif (self.show_since_date % 100)  == 0:
            return 1

    def first_notify(instance, *args, **kwargs):
        to_user = instance
        announcement = '안녕하세요! 꿈꾸는 개발자에 오신걸 환영합니다<br> 문의나 제보사항은 페이지 하단 "문의 및 건의사항" 버튼을 눌러 보낼 수 있습니다.<br> 많은 의견 부탁드립니다!'
        if AdminNotification.objects.count() == 0 and not instance.is_active == True:
            notify = AdminNotification(to_user=to_user, announcement=announcement) # 메일 제일 처음에 받음 이걸로하면 안됨
            notify.save()
        else:
            pass

post_save.connect(User.first_notify, sender=User)


class Interest(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Stack(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Profile(models.Model):
    TYPE_CHOICES = (
        ('0', '개발자'),
        ('1', '디자이너'),
        ('2', '기획자'),
        ('3', '기타')
    )
    STATUS_CHOICES = (
        ('0', '휴식 중'),
        ('1', '팀 찾는 중'),
        ('2', '팀 참가 중'),
        ('3', '기타')
    )
    OPEN_CHOICES = ((False, '학교'), (True, '전체'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.SlugField(max_length=10, unique=True, allow_unicode=True)
    self_intro = models.TextField(blank=True)

    github = models.URLField(blank=True)
    email = models.EmailField(blank=True)

    image = models.ImageField(upload_to='profile/', default='../static/img/profile-default.png') # media 밑에 profile 폴더 생성
    type = models.CharField(choices=TYPE_CHOICES, max_length=2, default='0')
    status = models.CharField(choices=STATUS_CHOICES, max_length=2, default='3')
    has_entered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    to_open = models.BooleanField(default=True, choices=OPEN_CHOICES)

    interest = models.ManyToManyField(Interest, blank=True)
    stack = models.ManyToManyField(Stack, blank=True)

    def __str__(self):
        return self.nickname





class Activity(models.Model):
    ACTIVITY_CHOICES = (
        ('0', '동아리'),
        ('1', '프로젝트'),
        ('2', '기타')
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='activity')
    name = models.CharField(max_length=20)
    type = models.CharField(choices=ACTIVITY_CHOICES, max_length=1, default='0')
    role = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Award(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='award')
    name = models.CharField(max_length=20)
    result = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=20, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Intern(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='intern')
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    LANGUAGE_ABILITY_CHOICES = (
        ('0', '초급 (기본적인 대화 가능)'),
        ('1', '중급 (사무적인 대화 가능)'),
        ('2', '고급 (자유자재 의사소통)')
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='language')
    name = models.CharField(max_length=10)
    ability = models.CharField(choices=LANGUAGE_ABILITY_CHOICES, max_length=1, default='0')

    def __str__(self):
        return self.name


class Certificate(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certificate')
    name = models.CharField(max_length=30)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class AdvertiseMail(models.Model):
    date = models.DateTimeField(default=timezone.now)
    subject = models.CharField(max_length=100)
    mail = models.TextField(blank=False, null=True)
    send_it = models.BooleanField(default=False)

    def save(self):
        if self.send_it:
            all_users = get_user_model().objects.all()
            for user in all_users:
                send_mail(str(self.subject),
                          '',
                          'from.devdreamer@gmail.com',
                          [user.email],
                          html_message=self.mail,
                          fail_silently=False)
