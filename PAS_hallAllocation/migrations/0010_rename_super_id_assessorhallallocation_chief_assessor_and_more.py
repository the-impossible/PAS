# Generated by Django 4.1.2 on 2022-12-14 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_app', '0013_title'),
        ('PAS_auth', '0025_supervisorprofile_super_nd'),
        ('PAS_hallAllocation', '0009_studhallallocation_type_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assessorhallallocation',
            old_name='super_id',
            new_name='chief_assessor',
        ),
        migrations.RemoveField(
            model_name='assessorhallallocation',
            name='isChief',
        ),
        migrations.AddField(
            model_name='assessorhallallocation',
            name='assessor_one',
            field=models.ForeignKey(default='032f56ac492e4274a4303af9f85beea0', on_delete=django.db.models.deletion.CASCADE, related_name='assessor_one', to='PAS_auth.supervisorprofile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assessorhallallocation',
            name='assessor_two',
            field=models.ForeignKey(default='032f56ac492e4274a4303af9f85beea0', on_delete=django.db.models.deletion.CASCADE, related_name='assessor_two', to='PAS_auth.supervisorprofile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assessorhallallocation',
            name='type_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='PAS_app.studenttype'),
            preserve_default=False,
        ),
    ]