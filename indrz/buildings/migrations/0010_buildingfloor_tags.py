# Generated by Django 3.1.13 on 2021-08-29 10:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0009_interiorfloorsection_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingfloor',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None), blank=True, null=True, size=None),
        ),
    ]
