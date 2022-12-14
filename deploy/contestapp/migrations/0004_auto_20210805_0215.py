# Generated by Django 3.2.5 on 2021-08-05 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contestapp', '0003_alter_contest_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='finish_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='participant',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
