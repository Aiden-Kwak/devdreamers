# Generated by Django 3.2.5 on 2021-09-18 23:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notificationapp', '0005_notification_announcement_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='announcement',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='announcement_link',
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(choices=[(1, 'TeamComment'), (2, 'NewContest')]),
        ),
        migrations.CreateModel(
            name='ContestNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_has_seen', models.BooleanField(default=False)),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contest_notify', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdminNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_has_seen', models.BooleanField(default=False)),
                ('announcement', models.TextField(blank=True, null=True)),
                ('announcement_link', models.CharField(blank=True, default='/', max_length=200, null=True)),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='announcement_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
