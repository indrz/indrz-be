# Generated by Django 3.1.13 on 2021-09-08 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poi_manager', '0014_auto_20210829_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='poicategory',
            name='html_field',
            field=models.TextField(blank=True, null=True, verbose_name='HTML for popups'),
        ),
    ]