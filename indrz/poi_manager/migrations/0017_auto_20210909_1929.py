# Generated by Django 3.1.13 on 2021-09-09 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poi_manager', '0016_auto_20210909_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poicategory',
            name='html_content',
            field=models.TextField(blank=True, null=True, verbose_name='HTML content'),
        ),
    ]
