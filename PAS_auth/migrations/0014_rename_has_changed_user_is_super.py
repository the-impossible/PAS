# Generated by Django 4.0.6 on 2022-09-06 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_auth', '0013_remove_allocate_group_num_allocate_group_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='has_changed',
            new_name='is_super',
        ),
    ]
