# Generated by Django 4.1.1 on 2022-10-01 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_auth', '0023_alter_supervisorprofile_capacity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supervisorprofile',
            name='capacity',
        ),
        migrations.AddField(
            model_name='supervisorprofile',
            name='Ev_capacity',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='supervisorprofile',
            name='RG_capacity',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
