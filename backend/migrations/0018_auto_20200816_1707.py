# Generated by Django 3.0.8 on 2020-08-16 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_activity_raw_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='latitude',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='activity',
            name='longitude',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='activity',
            name='polyline',
            field=models.TextField(blank=True, null=True),
        ),
    ]