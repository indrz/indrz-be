# Generated by Django 2.2.6 on 2019-11-22 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poi_manager', '0007_auto_20191122_0739'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poi',
            old_name='fk_poi_category',
            new_name='category',
        ),
    ]