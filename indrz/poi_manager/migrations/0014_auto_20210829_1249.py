# Generated by Django 3.1.13 on 2021-08-29 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poi_manager', '0013_auto_20210106_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poiicon',
            name='icon',
            field=models.ImageField(default='/poi_icons/other_pin.png', max_length=512, upload_to='poi_icons', verbose_name='Poi icon image'),
        ),
    ]