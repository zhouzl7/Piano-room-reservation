# Generated by Django 2.1.3 on 2018-12-10 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PRmanage', '0037_auto_20181210_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pianoroom',
            name='room_id',
            field=models.CharField(max_length=12, unique=True, verbose_name='编号'),
        ),
    ]
