# Generated by Django 3.0.8 on 2020-08-01 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
