# Generated by Django 2.2.6 on 2019-11-29 20:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0005_auto_20191113_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingfloorspace',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=150), blank=True, null=True, size=None), blank=True, null=True, size=None),
        ),
    ]