# Generated by Django 2.0.2 on 2018-11-29 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PRmanage', '0015_auto_20181121_1820'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetable',
            name='date',
        ),
    ]
