# Generated by Django 4.0.6 on 2022-09-07 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_auth', '0015_user_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSendCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'EmailCounter',
            },
        ),
    ]
