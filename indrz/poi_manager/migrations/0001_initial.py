# Generated by Django 2.2.5 on 2019-10-01 19:25

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('buildings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoiIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name of map icon')),
                ('poi_icon', models.FileField(max_length=512, upload_to='media/poi_icons', verbose_name='Poi icon image')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='PoiCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Category name')),
                ('icon_css_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Icon CSS name')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='description')),
                ('force_mid_point', models.NullBooleanField(verbose_name='Force route to this location')),
                ('enabled', models.NullBooleanField(verbose_name='Activated and enabled')),
                ('tree_order', models.IntegerField(blank=True, null=True, verbose_name='Tree order in legend')),
                ('sort_order', models.IntegerField(blank=True, null=True, verbose_name='Sort oder of POI items')),
                ('cat_name_en', models.CharField(blank=True, max_length=255, null=True)),
                ('cat_name_de', models.CharField(blank=True, max_length=255, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('fk_poi_icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='poi_manager.PoiIcon')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, default=9999, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='poi_manager.PoiCategory')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Poi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('floor_num', models.IntegerField(blank=True, null=True, verbose_name='floor number')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='description')),
                ('enabled', models.NullBooleanField(verbose_name='Activated and enabled')),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(blank=True, db_column='geom', null=True, srid=3857)),
                ('poi_tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), blank=True, null=True, size=None)),
                ('name_en', models.CharField(blank=True, max_length=255, null=True)),
                ('name_de', models.CharField(blank=True, max_length=255, null=True)),
                ('fk_building', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='buildings.Building')),
                ('fk_building_floor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='buildings.BuildingFloor')),
                ('fk_campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings.Campus')),
                ('fk_poi_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poi_manager.PoiCategory')),
            ],
        ),
    ]
