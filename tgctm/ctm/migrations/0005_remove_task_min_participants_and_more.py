# Generated by Django 4.1.7 on 2023-03-21 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctm', '0004_alter_profile_timeslot_crewuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='min_participants',
        ),
        migrations.AddField(
            model_name='tasktimeslot',
            name='max_participants',
            field=models.IntegerField(blank=True, default=10),
            preserve_default=False,
        ),
    ]
