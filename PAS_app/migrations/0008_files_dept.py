# Generated by Django 4.0.6 on 2022-08-19 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_app', '0007_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='dept',
            field=models.ForeignKey(default='392b7620d3c74e92a1e15a3e18e5937d', on_delete=django.db.models.deletion.CASCADE, to='PAS_app.department'),
            preserve_default=False,
        ),
    ]
