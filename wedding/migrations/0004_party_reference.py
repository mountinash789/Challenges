# Generated by Django 3.0.8 on 2020-10-03 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0003_party_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='reference',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]