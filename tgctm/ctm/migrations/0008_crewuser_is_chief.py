# Generated by Django 4.1.7 on 2023-03-22 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctm', '0007_alter_checkinusertasktimeslot_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='crewuser',
            name='is_chief',
            field=models.BooleanField(default=False),
        ),
    ]
