# Generated by Django 3.0.8 on 2020-08-02 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20200802_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='userconnection',
            name='access_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userconnection',
            name='expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userconnection',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
