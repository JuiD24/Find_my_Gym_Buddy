# Generated by Django 3.2.9 on 2021-11-12 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_activitymodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activitymodel',
            old_name='added_on',
            new_name='activity_added_on',
        ),
    ]
