# Generated by Django 3.2.5 on 2021-10-02 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notificationapp', '0008_auto_20210919_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcementfield',
            name='announcement_admin',
            field=models.TextField(null=True),
        ),
    ]
