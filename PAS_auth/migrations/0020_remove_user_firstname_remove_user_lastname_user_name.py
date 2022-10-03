# Generated by Django 4.1.1 on 2022-10-01 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_auth', '0019_supervisorprofile_prog_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='lastname',
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=60),
        ),
    ]