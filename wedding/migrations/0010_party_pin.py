# Generated by Django 3.0.8 on 2021-02-15 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0009_auto_20210215_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='pin',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]