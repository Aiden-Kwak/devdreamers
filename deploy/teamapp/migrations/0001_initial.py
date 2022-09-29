# Generated by Django 3.2.5 on 2021-07-08 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, null=True, verbose_name='TITLE')),
                ('description', models.CharField(blank=True, help_text='simple description text.', max_length=45, null=True, verbose_name='DESCRIPTION')),
                ('category', models.CharField(choices=[('0', '스터디'), ('1', '프로젝트'), ('2', '대회/공모전'), ('3', '동아리'), ('4', '스타트업')], default='0', max_length=2)),
                ('dev_tags', multiselectfield.db.fields.MultiSelectField(choices=[('서버/백엔드', '서버/백엔드'), ('프론트엔드', '프론트엔드'), ('DevOps', 'DevOps'), ('안드로이드 앱', '안드로이드 앱'), ('아이폰 앱', '아이폰 앱'), ('UI/UX', 'UI/UX'), ('데이터 엔지니어', '데이터 엔지니어'), ('머신러닝/AI', '머신러닝/AI'), ('게임 개발', '게임 개발'), ('AR/VR', 'AR/VR'), ('그래픽 디자인', '그래픽 디자인'), ('임베디드', '임베디드'), ('IoT', 'IoT'), ('보안', '보안'), ('블록체인', '블록체인'), ('알고리즘', '알고리즘'), ('기획/PM', '기획/PM'), ('마케팅', '마케팅'), ('기타', '기타')], max_length=111, null=True)),
                ('content', models.TextField(default='<h3>* 설명이 풍부한 모집글은 팀에 대해 더 많은 관심을 가지게합니다!</h3><p><br></p><p>(작성 예시)</p><p>1. 프로젝트 필요성 (팀의 목적에 대해 설명합니다!)</p><p>2. 출시 플랫폼 (만약 출시를 목적으로 한다면&nbsp;React Native Android, IOS 등 출시 계획을 넣어보는 건 어떨까요?)</p><p>3. 개발 환경 (프론트엔드, 백엔드, db 등 개발 환경에 대해 설명합니다!)</p><p>4. 이런분들을 원합니다! (특정 기술스택에 대한 실력자가 필요하다거나, 실력은 없어도 노력하는 인재가 필요하다거나 필요한 인재상을 적어보아요.)</p><p>5. 진행현황 (무엇을 하는 팀인지를 지원자들이 더 명확히 알 수 있겠죠?)</p><p>6. 기타사항</p>', null=True, verbose_name='CONTENT')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='CREATE DATE')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='MODIFY DATE')),
                ('team_color', models.CharField(default='rgba(240, 116, 137, 1)', max_length=25, null=True, verbose_name='COLOR')),
                ('deadline', models.DateTimeField(null=True)),
                ('contact', models.CharField(max_length=1024, null=True)),
                ('image', models.ImageField(blank=True, default='../static/img/team-default.jpg', upload_to='team/')),
                ('visible', models.BooleanField(default=True)),
                ('to_open', models.BooleanField(choices=[(False, '자신 학교에만 공개하기'), (True, '모든 학교에 공개하기')], default=False)),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]