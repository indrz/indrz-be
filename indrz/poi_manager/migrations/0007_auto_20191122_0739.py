# Generated by Django 2.2.6 on 2019-11-22 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poi_manager', '0006_poi_fk_campus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poi',
            name='fk_building',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='buildings.Building'),
        ),
        migrations.AlterField(
            model_name='poi',
            name='fk_building_floor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='buildings.BuildingFloor'),
        ),
        migrations.AlterField(
            model_name='poi',
            name='fk_campus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='buildings.Campus'),
        ),
    ]
