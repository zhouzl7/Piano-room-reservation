# Generated by Django 2.0.2 on 2018-11-20 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PRmanage', '0010_timetable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='Time',
            field=models.DurationField(verbose_name='1th'),
        ),
    ]
