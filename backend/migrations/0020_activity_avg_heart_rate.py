# Generated by Django 3.0.8 on 2020-08-16 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_activity_moving_duration_seconds'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='avg_heart_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
