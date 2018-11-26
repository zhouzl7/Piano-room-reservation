# Generated by Django 2.0.2 on 2018-11-18 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('USERmanage', '0005_auto_20181118_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='USERmanage.UserGroup', verbose_name='用户组'),
        ),
        migrations.AlterField(
            model_name='user',
            name='open_id',
            field=models.CharField(blank=True, db_index=True, max_length=64, unique=True, verbose_name='open_id'),
        ),
    ]
