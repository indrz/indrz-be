# Generated by Django 2.2.6 on 2019-11-22 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poi_manager', '0008_auto_20191122_0744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poi',
            old_name='fk_campus',
            new_name='campus',
        ),
        migrations.RenameField(
            model_name='poi',
            old_name='fk_building_floor',
            new_name='floor',
        ),
        migrations.RemoveField(
            model_name='poi',
            name='fk_building',
        ),
    ]