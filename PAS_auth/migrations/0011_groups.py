# Generated by Django 4.0.6 on 2022-09-01 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_auth', '0010_alter_allocate_type_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_num', models.CharField(max_length=100)),
            ],
        ),
    ]
