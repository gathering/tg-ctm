# Generated by Django 4.1.7 on 2023-04-06 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctm', '0008_crewuser_is_chief'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktimeslotuser',
            name='reminder_status',
            field=models.CharField(choices=[('NO', 'None'), ('ON', 'Once'), ('TW', 'Twice')], default='NO', max_length=2),
        ),
    ]
