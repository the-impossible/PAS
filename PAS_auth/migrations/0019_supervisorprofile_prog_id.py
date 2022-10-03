# Generated by Django 4.1.1 on 2022-09-24 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_app', '0011_remove_supervisorrank_rank_title_and_more'),
        ('PAS_auth', '0018_remove_studentprofile_pic_user_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='supervisorprofile',
            name='prog_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='PAS_app.programme'),
            preserve_default=False,
        ),
    ]