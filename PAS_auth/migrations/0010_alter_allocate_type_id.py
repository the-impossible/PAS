# Generated by Django 4.0.6 on 2022-08-29 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_app', '0011_remove_supervisorrank_rank_title_and_more'),
        ('PAS_auth', '0009_allocate_type_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocate',
            name='type_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='PAS_app.studenttype'),
            preserve_default=False,
        ),
    ]
