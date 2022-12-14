# Generated by Django 3.2.5 on 2021-07-19 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountapp', '0002_remove_profile_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='to_open',
            field=models.BooleanField(choices=[(False, '자신 학교에만 공개하기'), (True, '모든 학교에 공개하기')], default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.CharField(choices=[('0', '성균관대학교')], max_length=2, null=True),
        ),
    ]
