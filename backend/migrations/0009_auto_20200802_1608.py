# Generated by Django 3.0.8 on 2020-08-02 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_userconnection_last_pulled'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='total_elevation_gain',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='activity',
            name='distance_meters',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='activity',
            name='duration_seconds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
