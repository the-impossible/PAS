# Generated by Django 4.0.6 on 2022-08-19 16:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_app', '0006_delete_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('dept_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('dept_title', models.CharField(max_length=30, unique=True)),
                ('dept_desc', models.CharField(blank=True, max_length=100, null=True)),
                ('dept_logo', models.ImageField(blank=True, null=True, upload_to='uploads/department/')),
            ],
            options={
                'verbose_name_plural': 'Departments',
                'db_table': 'Department',
            },
        ),
    ]
