# Generated by Django 2.1.3 on 2018-12-06 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PRmanage', '0029_auto_20181206_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='piano_room',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='PRmanage.PianoRoom', to_field='room_id', verbose_name='琴房'),
        ),
    ]
