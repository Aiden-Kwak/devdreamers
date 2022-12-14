# Generated by Django 3.2.5 on 2021-09-08 21:57

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contestapp', '0008_alter_contest_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('SW', 'SW'), ('웹/앱 개발', '웹/앱 개발'), ('게임', '게임'), ('보안', '보안'), ('AI/빅데이터', 'AI/빅데이터'), ('알고리즘', '알고리즘'), ('임베디드', '임베디드'), ('로봇/자율주행', '로봇/자율주행'), ('기타', '기타')], max_length=44, null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='title',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
