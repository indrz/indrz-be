# Generated by Django 2.2.6 on 2019-12-07 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poi_manager', '0011_auto_20191207_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poiicon',
            name='poi_icon',
            field=models.ImageField(max_length=512, upload_to='poi-icons', verbose_name='Poi icon image'),
        ),
    ]
