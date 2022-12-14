# Generated by Django 3.2.5 on 2021-07-19 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamapp', '0002_auto_20210715_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='content',
            field=models.TextField(null=True, verbose_name='CONTENT'),
        ),
        migrations.AlterField(
            model_name='team',
            name='to_open',
            field=models.BooleanField(choices=[(False, '자신 학교에만 공개하기'), (True, '모든 학교에 공개하기')], default=True),
        ),
    ]
