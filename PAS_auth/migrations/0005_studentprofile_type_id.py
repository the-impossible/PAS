# Generated by Django 4.0.6 on 2022-08-22 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_app', '0010_files_used_supervisorsfiles_used'),
        ('PAS_auth', '0004_supervisorprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='type_id',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='PAS_app.studenttype'),
        ),
    ]
