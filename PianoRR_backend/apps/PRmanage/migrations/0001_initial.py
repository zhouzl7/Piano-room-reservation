# Generated by Django 2.0.2 on 2018-11-15 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PianoRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(db_index=True, max_length=10, unique=True)),
                ('piano_type', models.CharField(max_length=20)),
                ('open_time', models.DateTimeField(db_index=True)),
                ('close_time', models.DateTimeField(db_index=True)),
                ('status', models.IntegerField()),
            ],
            options={
                'verbose_name': '琴房信息',
                'verbose_name_plural': '琴房信息',
            },
        ),
    ]
