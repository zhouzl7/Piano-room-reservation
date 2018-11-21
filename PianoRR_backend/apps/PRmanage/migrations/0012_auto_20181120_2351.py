# Generated by Django 2.0.2 on 2018-11-20 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PRmanage', '0011_auto_20181120_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetable',
            name='Time',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='close_time',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='open_time',
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time1',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='8：00-9：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time10',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='17：00-18：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time11',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='18：00-19：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time12',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='19：00-20：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time13',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='20：00-21：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time14',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='21：00-22：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time2',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='9：00-10：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time3',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='10：00-11：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time4',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='11：00-12：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time5',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='12：00-13：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time6',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='13：00-14：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time7',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='14：00-15：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time8',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='15：00-16：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='Time9',
            field=models.BooleanField(choices=[(True, '开放'), (False, '关闭')], default=True, verbose_name='16：00-17：00'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='piano_room',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='PRmanage.PianoRoom', verbose_name='琴房'),
        ),
        migrations.AlterField(
            model_name='pianoroom',
            name='status',
            field=models.BooleanField(choices=[(True, '开放使用'), (False, '关闭使用')], default=True, verbose_name='状态'),
        ),
    ]