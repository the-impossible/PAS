# Generated by Django 4.1.2 on 2022-11-30 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PAS_assessment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daysofdefense',
            name='num_of_day',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='studhallallocation',
            name='day_num',
            field=models.IntegerField(default=1),
        ),
    ]
