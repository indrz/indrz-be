# Generated by Django 2.2.6 on 2020-03-01 08:39

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0008_auto_20191208_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='interiorfloorsection',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None), blank=True, null=True, size=None),
        ),
    ]