# Generated by Django 2.0.2 on 2018-11-21 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PRmanage', '0014_auto_20181121_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='Time1',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='08-09'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time10',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='17-18'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time11',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='18-19'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time12',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='19-20'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time13',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='20-21'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time14',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='21-22'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time2',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='09-10'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time3',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='10-11'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time4',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='11-12'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time5',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='12-13'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time6',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='13-14'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time7',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='14-15'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time8',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='15-16'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Time9',
            field=models.IntegerField(choices=[(-1, '停止使用'), (0, '已被预约'), (1, '可被预约')], default=1, verbose_name='16-17'),
        ),
    ]
