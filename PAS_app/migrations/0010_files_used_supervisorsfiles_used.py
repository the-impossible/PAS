# Generated by Django 4.0.6 on 2022-08-21 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_app', '0009_supervisorsfiles_dept'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='used',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='supervisorsfiles',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]