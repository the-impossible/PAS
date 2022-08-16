# Generated by Django 4.0.6 on 2022-08-15 16:41

import PAS_app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme_title', models.CharField(max_length=30, unique=True)),
                ('programme_description', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Programmes',
                'db_table': 'Programme',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_title', models.CharField(max_length=9, unique=True)),
                ('session_description', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Sessions',
                'db_table': 'Session',
            },
        ),
        migrations.CreateModel(
            name='StudentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_title', models.CharField(max_length=30, unique=True)),
                ('type_description', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Student Types',
                'db_table': 'StudentType',
            },
        ),
        migrations.CreateModel(
            name='SupervisorRank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank_title', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('rank_description', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Supervisor Rank',
                'db_table': 'Supervisor Rank',
            },
        ),
        migrations.CreateModel(
            name='SupervisorsFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=PAS_app.models.path_and_rename)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PAS_app.programme')),
                ('supervisor_rank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PAS_app.supervisorrank')),
            ],
            options={
                'verbose_name_plural': 'Supervisors Files',
                'db_table': 'Supervisors File',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=PAS_app.models.path_and_rename)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PAS_app.programme')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PAS_app.session')),
                ('student_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PAS_app.studenttype')),
            ],
            options={
                'verbose_name_plural': 'Files',
                'db_table': 'File',
            },
        ),
    ]